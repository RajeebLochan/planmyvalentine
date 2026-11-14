from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import ValentinePlan, Reaction, LoveLetter
from .forms import PlannerForm, ReactionForm
from core.prompts import generate_plan_with_ai, generate_love_letter
from core.utils import generate_share_code
import json


def planner_form(request):
    """Display and process the planner form"""
    
    # Get relationship type from query param (for direct links)
    relationship_type = request.GET.get('type', '')
    
    if request.method == 'POST':
        form = PlannerForm(request.POST)
        if form.is_valid():
            # Save the form but don't commit yet
            plan = form.save(commit=False)
            
            # Generate share code
            plan.share_code = generate_share_code(plan.your_name, plan.partner_name)
            
            # Get user IP (optional)
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                plan.creator_ip = x_forwarded_for.split(',')[0]
            else:
                plan.creator_ip = request.META.get('REMOTE_ADDR')
            
            # Generate AI plan
            user_data = {
                'your_name': plan.your_name,
                'partner_name': plan.partner_name,
                'relationship_type': plan.relationship_type,
                'city': plan.city,
                'budget': plan.budget,
                'plan_type': plan.plan_type,
                'vibe': plan.vibe,
                'about_partner': plan.about_partner,
                'about_yourself': plan.about_yourself,
                'special_request': plan.special_request,
            }
            
            plan.plan_content = generate_plan_with_ai(user_data)
            
            # Save to database
            plan.save()
            
            # Store plan ID in session for easy access
            request.session['last_plan_id'] = str(plan.plan_id)
            
            # Redirect to result page
            return redirect('planner:result', share_code=plan.share_code)
    else:
        # Pre-fill relationship type if provided
        initial = {}
        if relationship_type:
            initial['relationship_type'] = relationship_type
        form = PlannerForm(initial=initial)
    
    context = {
        'form': form,
        'relationship_type': relationship_type,
    }
    return render(request, 'planner_form.html', context)


def result(request, share_code):
    """Display the generated plan"""
    
    plan = get_object_or_404(ValentinePlan, share_code=share_code)
    
    # Increment view count
    plan.increment_views()
    
    # Check if user is the creator (for showing extra options)
    is_creator = str(plan.plan_id) == request.session.get('last_plan_id', '')
    
    # Get reactions count
    reactions_count = {}
    for reaction in Reaction.objects.filter(plan=plan).values('reaction_type'):
        reaction_type = reaction['reaction_type']
        reactions_count[reaction_type] = reactions_count.get(reaction_type, 0) + 1
    
    # Check if love letter exists
    has_love_letter = hasattr(plan, 'love_letter')
    
    context = {
        'plan': plan,
        'is_creator': is_creator,
        'reactions_count': reactions_count,
        'has_love_letter': has_love_letter,
        'share_url': request.build_absolute_uri(),
    }
    return render(request, 'result.html', context)


def share(request, share_code):
    """Public share page (can be anonymous)"""
    
    plan = get_object_or_404(ValentinePlan, share_code=share_code)
    
    # Increment view count
    plan.increment_views()
    
    # Show different message if it's anonymous
    is_anonymous = plan.is_anonymous
    
    # Get reactions count
    reactions_count = {}
    for reaction in Reaction.objects.filter(plan=plan).values('reaction_type'):
        reaction_type = reaction['reaction_type']
        reactions_count[reaction_type] = reactions_count.get(reaction_type, 0) + 1
    
    # Reaction form
    reaction_form = ReactionForm()
    
    context = {
        'plan': plan,
        'is_anonymous': is_anonymous,
        'reactions_count': reactions_count,
        'reaction_form': reaction_form,
        'share_url': request.build_absolute_uri(),
    }
    return render(request, 'share.html', context)


@require_http_methods(["POST"])
def add_reaction(request, share_code):
    """Add a reaction to a plan"""
    
    plan = get_object_or_404(ValentinePlan, share_code=share_code)
    
    reaction_type = request.POST.get('reaction_type')
    
    if reaction_type:
        # Get user IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            reactor_ip = x_forwarded_for.split(',')[0]
        else:
            reactor_ip = request.META.get('REMOTE_ADDR')
        
        # Create reaction
        Reaction.objects.create(
            plan=plan,
            reaction_type=reaction_type,
            reactor_ip=reactor_ip
        )
        
        messages.success(request, 'Reaction added')
    
    return redirect('planner:share', share_code=share_code)


@require_http_methods(["POST"])
def generate_letter(request, share_code):
    """Generate a love letter for the plan"""
    
    plan = get_object_or_404(ValentinePlan, share_code=share_code)
    
    # Check if letter already exists
    if hasattr(plan, 'love_letter'):
        return redirect('planner:view_letter', share_code=share_code)
    
    # Generate love letter
    user_data = {
        'your_name': plan.your_name,
        'partner_name': plan.partner_name,
        'relationship_type': plan.relationship_type,
    }
    
    letter_content = generate_love_letter(user_data)
    
    # Save letter
    LoveLetter.objects.create(
        plan=plan,
        your_name=plan.your_name,
        partner_name=plan.partner_name,
        letter_content=letter_content
    )
    
    messages.success(request, 'Your letter is ready')
    return redirect('planner:view_letter', share_code=share_code)


def view_letter(request, share_code):
    """View the love letter"""
    
    plan = get_object_or_404(ValentinePlan, share_code=share_code)
    
    if not hasattr(plan, 'love_letter'):
        messages.error(request, 'No letter yet. Write one from your plan first')
        return redirect('planner:result', share_code=share_code)
    
    context = {
        'plan': plan,
        'letter': plan.love_letter,
    }
    return render(request, 'letter.html', context)


def make_anonymous(request, share_code):
    """Convert a plan to anonymous/confession mode"""
    
    plan = get_object_or_404(ValentinePlan, share_code=share_code)
    
    # Only creator can do this
    if str(plan.plan_id) == request.session.get('last_plan_id', ''):
        plan.is_anonymous = True
        plan.save()
        messages.success(request, 'Confession mode is on. Your name is hidden on the shared link')
    else:
        messages.error(request, 'You can only do this for your own plans.')
    
    return redirect('planner:result', share_code=share_code)


def reveal_sender(request, share_code):
    """Reveal who sent the plan (toggle anonymous mode)"""
    
    plan = get_object_or_404(ValentinePlan, share_code=share_code)
    
    # Only creator can do this
    if str(plan.plan_id) == request.session.get('last_plan_id', ''):
        plan.is_anonymous = False
        plan.save()
        messages.success(request, 'Your name is now shown on the shared link')
    else:
        messages.error(request, 'You can only do this for your own plans.')
    
    return redirect('planner:share', share_code=share_code)
