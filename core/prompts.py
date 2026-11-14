"""
OpenAI Integration and Prompt Templates for PlanMyValentine
"""
import os
import re
import openai
from django.conf import settings


def format_plan_content(content):
    """Format AI response to proper HTML"""
    # Convert markdown-style bold to HTML
    content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
    
    # Convert headers
    content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
    
    # Convert line breaks to paragraphs
    paragraphs = content.split('\n\n')
    formatted_paragraphs = []
    
    for para in paragraphs:
        if para.strip():
            if not para.strip().startswith('<'):
                if para.strip().startswith(('-', '*', '•')):
                    items = para.strip().split('\n')
                    list_html = '<ul>'
                    for item in items:
                        item = item.lstrip('-*• ').strip()
                        if item:
                            list_html += f'<li>{item}</li>'
                    list_html += '</ul>'
                    formatted_paragraphs.append(list_html)
                else:
                    formatted_paragraphs.append(f'<p>{para.strip()}</p>')
            else:
                formatted_paragraphs.append(para)
    
    return '\n'.join(formatted_paragraphs)

# City-specific suggestions with romantic intelligence
CITY_SUGGESTIONS = {
    # ==================== ODISHA CITIES ====================
    'bhubaneswar': {
        'display_name': 'Bhubaneswar',
        'tagline': 'The Temple City of Love',
        'romantic_desc': 'Where ancient temples whisper timeless love stories and serene lakes set the mood for forever.',
        'state': 'Odisha',
        'places': ['Lingaraj Temple', 'Nandankanan Zoo', 'Dhauli Shanti Stupa', 'Ekamra Haat', 'Rajarani Temple', 'Udayagiri & Khandagiri Caves'],
        'cafes': ['The Zaika', 'Celesta Lounge', 'Cafe Coffee Day - Saheed Nagar', 'Brewberrys Cafe', 'Dalma Restaurant', 'Barbeque Nation'],
        'activities': ['Evening walk at Chandrasekhar Azad Park', 'Boat ride at Bindu Sarovar', 'Shopping at Janpath', 'Heritage walk at Old Town'],
        'romantic_spots': ['Sunset at Dhauli Peace Pagoda', 'Rajarani Temple garden stroll', 'Khandagiri caves at golden hour', 'Nicco Park evening'],
        'hotels': ['Hotel Mirka Plaza','Mayfair Lagoon', 'Swosti Premium', 'Trident Bhubaneswar', 'Lemon Tree Premier'],
        'date_ideas': ['Temple trail at sunrise', 'Candlelight dinner at Mayfair Lagoon', 'Picnic at Nandankanan gardens'],
        'hero_emoji': '🏛️',
    },
    'cuttack': {
        'display_name': 'Cuttack',
        'tagline': 'The Silver City of Eternal Bonds',
        'romantic_desc': 'Where the Mahanadi flows like a love song and silver filigree captures the delicacy of every heartbeat.',
        'state': 'Odisha',
        'places': ['Barabati Fort', 'Netaji Birth Place Museum', 'Dhabaleswar Island', 'Cuttack Chandi Temple', 'Stone Revetment (Kathjodi River)'],
        'cafes': ['Mangalam Restaurant', 'Odisha Hotel', 'Cafe Coffee Day - College Square', 'Dominos - Badambadi', 'Desi Kitchen'],
        'activities': ['Boat ride to Dhabaleswar Island', 'Silver filigree shopping at Nayasarak', 'Evening stroll at Stone Revetment', 'Heritage walk at Barabati Fort'],
        'romantic_spots': ['Dhabaleswar Island temple at sunset', 'Barabati Fort garden evening', 'Kathjodi River bank at dusk', 'Jobra barrage walk'],
        'hotels': ['Mayfair Heritage', 'Hotel Grand Central', 'Hotel Akbari Residency', 'Hotel Konark'],
        'date_ideas': ['Boat trip to Dhabaleswar temple', 'Silver shopping + chai at Nayasarak', 'Sunset walk at Jobra barrage'],
        'hero_emoji': '🪙',
    },
    'puri': {
        'display_name': 'Puri',
        'tagline': 'Where the Sea Blesses Love',
        'romantic_desc': 'Golden sands, sacred shores, and sunrises that paint the sky — Puri is where devotion meets desire.',
        'state': 'Odisha',
        'places': ['Jagannath Temple', 'Puri Beach', 'Chilika Lake', 'Konark Sun Temple', 'Raghurajpur Artist Village'],
        'cafes': ['Chung Wah', 'Wildgrass Restaurant', 'Peace Restaurant', 'Honey Bee Bakery', 'Gandhara Restaurant'],
        'activities': ['Sunrise at Puri Beach', 'Day trip to Konark Sun Temple', 'Dolphin watching at Chilika Lake', 'Sand art viewing'],
        'romantic_spots': ['Puri Beach sunrise', 'Chandrabhaga Beach near Konark', 'Chilika Lake boat ride at sunset', 'Beachside bonfire evening'],
        'hotels': ['Mayfair Waves', 'Toshali Sands', 'Hans Coco Palms', 'Hotel Naren Palace'],
        'date_ideas': ['Sunrise beach walk + breakfast', 'Day trip to Konark together', 'Chilika Lake dolphin cruise'],
        'hero_emoji': '🌊',
    },
    'rourkela': {
        'display_name': 'Rourkela',
        'tagline': 'Steel City with a Soft Heart',
        'romantic_desc': 'Hills, rivers, and the raw beauty of tribal Odisha — Rourkela is love in its most untouched form.',
        'state': 'Odisha',
        'places': ['Hanuman Vatika', 'Vedvyas Temple', 'Koel River', 'Pitamahal Dam', 'Indira Gandhi Park', 'Darjeeng Hills'],
        'cafes': ['Rolls Mania', 'Bakers Street', 'Cafe Jeju', 'Nescafe Hub - NIT Rourkela', 'Dominos - Udit Nagar'],
        'activities': ['Picnic at Mandira Dam', 'Drive to Darjeeng Hills', 'Evening at Indira Gandhi Park', 'Visit tribal haat market'],
        'romantic_spots': ['Mandira Dam sunset', 'Vedvyas sangam (river confluence)', 'Darjeeng Hills viewpoint', 'Pitamahal Dam morning walk'],
        'hotels': ['Hotel Panthanivas', 'Mayfair Rourkela', 'Hotel Basant Residency', 'Hotel Bhagwati Palace'],
        'date_ideas': ['Sunrise drive to Darjeeng Hills', 'River picnic at Vedvyas', 'Candlelight dinner at Mayfair'],
        'hero_emoji': '⛰️',
    },
    'berhampur': {
        'display_name': 'Berhampur',
        'tagline': 'The Silk City of Sweet Whispers',
        'romantic_desc': 'Draped in silk and sweetness, Berhampur is where South Odisha love stories begin over chhena poda and temple bells.',
        'state': 'Odisha',
        'places': ['Tara Tarini Temple', 'Gopalpur-on-Sea', 'Nirmaljhar Waterfall', 'Jaugada Fort', 'Budhipadma Temple'],
        'cafes': ['Hotel & Restaurant Silk Route', 'Café Coffee Point', 'New Aashirwad Restaurant', 'Chat Bhandar', 'Peda stalls at Giri Road'],
        'activities': ['Beach day at Gopalpur', 'Visit Nirmaljhar Waterfall', 'Silk saree shopping at Giri Road', 'Evening at MKCG Medical College garden'],
        'romantic_spots': ['Gopalpur Beach sunset', 'Tara Tarini Hill ropeway', 'Nirmaljhar waterfall picnic', 'Aryapalli Beach (nearby)'],
        'hotels': ['Hotel & Resort Gopalpur Palm', 'Hotel & Restaurant Akash', 'Panthanivas Gopalpur', 'Hotel Padma'],
        'date_ideas': ['Road trip to Gopalpur Beach', 'Tara Tarini ropeway ride', 'Silk shopping + chhena poda date'],
        'hero_emoji': '🧣',
    },
    'sambalpur': {
        'display_name': 'Sambalpur',
        'tagline': 'Where Rivers & Hearts Dance Together',
        'romantic_desc': 'Sambalpuri handloom, Hirakud shores, and a sunset that paints love across the longest dam in the world.',
        'state': 'Odisha',
        'places': ['Hirakud Dam', 'Samaleswari Temple', 'Huma Leaning Temple', 'Deer Park', 'Cattle Island'],
        'cafes': ['Cafe Coffee Day - VSS Nagar', 'Hotel Sheela Towers Restaurant', 'Dominos Sambalpur', 'Chaat Bazaar at Khetrajpur'],
        'activities': ['Drive on Hirakud Dam road', 'Visit Huma Leaning Temple', 'Wildlife at Debrigarh Sanctuary', 'Shopping for Sambalpuri sarees'],
        'romantic_spots': ['Hirakud Dam sunset point (Gandhi Minar)', 'Cattle Island boat ride', 'Huma Temple riverside', 'Debrigarh lakeside morning'],
        'hotels': ['Hotel Sheela Towers', 'Hotel Uphar Palace', 'Panthanivas Hirakud', 'Hotel Sagar'],
        'date_ideas': ['Sunset at Hirakud Gandhi Minar', 'Boat ride to Cattle Island', 'Sambalpuri saree shopping together'],
        'hero_emoji': '🌅',
    },
    'balasore': {
        'display_name': 'Balasore',
        'tagline': 'The Coast of Quiet Love',
        'romantic_desc': 'Where the Bay of Bengal kisses the shore and Chandipur\'s magical vanishing sea leaves you breathless — just like love.',
        'state': 'Odisha',
        'places': ['Chandipur Beach', 'Panchalingeswar Temple', 'Kuldiha Forest', 'Sajanagarh Fort', 'Talasari Beach'],
        'cafes': ['Hotel Sagarika Restaurant', 'Cafe De Balasore', 'Odisha Hotel Balasore', 'Chandni Sweets', 'Paaka Restaurant'],
        'activities': ['Watch the vanishing sea at Chandipur', 'Trek to Panchalingeswar', 'Drive to Talasari Beach', 'Visit Sajanagarh Palace'],
        'romantic_spots': ['Chandipur Beach low-tide walk', 'Talasari Beach sunset', 'Panchalingeswar hill stream', 'Kuldiha forest safari morning'],
        'hotels': ['Hotel & Resort Chandipur', 'Panthanivas Chandipur', 'Hotel Sagarika', 'Hotel Sarangi'],
        'date_ideas': ['Morning at Chandipur vanishing sea', 'Talasari Beach picnic', 'Panchalingeswar temple trek'],
        'hero_emoji': '🐚',
    },
    'bhadrak': {
        'display_name': 'Bhadrak',
        'tagline': 'The Quiet Town with a Loud Heart',
        'romantic_desc': 'Small-town charm, Baitarani River breezes, and a simplicity that makes every moment together feel like a festival.',
        'state': 'Odisha',
        'places': ['Baitarani River Ghat', 'Akhandalamani Temple', 'Aradi Champeswar Temple', 'Dhamra Port Beach', 'Chandabali'],
        'cafes': ['Hotel Raj Palace Restaurant', 'Maa Tara Sweets', 'Local chai tapris at Station Road', 'Bhadrak Sweets & Snacks'],
        'activities': ['Evening at Baitarani River bank', 'Visit Akhandalamani Temple', 'Day trip to Dhamra Beach', 'Street food walk at Nayabazar'],
        'romantic_spots': ['Baitarani River sunset', 'Dhamra Beach serenity', 'Chandabali creek boat ride', 'Temple garden at Akhandalamani'],
        'hotels': ['Hotel Raj Palace', 'Hotel Sai Heritage', 'Hotel Utkal', 'Hotel Niladri'],
        'date_ideas': ['Riverside walk at Baitarani', 'Day trip to Dhamra Beach', 'Temple visit + sweet tasting'],
        'hero_emoji': '🌾',
    },
    'ganjam': {
        'display_name': 'Ganjam',
        'tagline': 'Where Every Sunset Tells a Love Story',
        'romantic_desc': 'Chilika shores, ancient forts, and the warmth of South Odisha — Ganjam is raw, real, and deeply romantic.',
        'state': 'Odisha',
        'places': ['Chilika Lake (Rambha side)', 'Gopalpur-on-Sea', 'Taptapani Hot Spring', 'Jaugada Fort', 'Potagarh Fort'],
        'cafes': ['Sea Shell Restaurant Gopalpur', 'Hotel Maa Tara', 'Rambha Lake View Restaurant', 'Panthanivas Restaurant'],
        'activities': ['Boating on Chilika Lake', 'Beach day at Gopalpur', 'Hot spring dip at Taptapani', 'Explore Jaugada ruins'],
        'romantic_spots': ['Chilika Lake sunset from Rambha', 'Gopalpur Beach moonlight', 'Taptapani forest walk', 'Potagarh Fort hilltop view'],
        'hotels': ['Panthanivas Gopalpur', 'Panthanivas Rambha', 'Hotel Sea Pearl', 'Taptapani Panthanivas'],
        'date_ideas': ['Chilika boat ride at dawn', 'Gopalpur Beach evening + dinner', 'Taptapani hot spring visit'],
        'hero_emoji': '🏖️',
    },
    'angul': {
        'display_name': 'Angul',
        'tagline': 'Love Hidden in the Green Hills',
        'romantic_desc': 'Surrounded by forests and waterfalls, Angul is where nature becomes the backdrop of your love story.',
        'state': 'Odisha',
        'places': ['Satkosia Tiger Reserve', 'Tikarpada', 'Badmul Eco Retreat', 'Satkoshia Gorge', 'Handapa Dam'],
        'cafes': ['Hotel Konark Restaurant', 'Chhotu Bhai Sweets', 'Highway Dhabas on NH55', 'Local tea stalls at Angul town'],
        'activities': ['Gorge boating at Satkosia', 'Nature walk at Tikarpada', 'Camping at Badmul', 'Bird watching at Satkosia'],
        'romantic_spots': ['Satkosia Gorge sunrise boat ride', 'Badmul riverside camping', 'Tikarpada forest trail', 'Handapa Dam sunset'],
        'hotels': ['Satkosia Eco Retreat (Badmul)', 'Tikarpada Nature Camp', 'Hotel Nilachal Angul', 'Hotel Sai Palace'],
        'date_ideas': ['Gorge boating at Satkosia', 'Overnight camping at Badmul', 'Wildlife safari at Tikarpada'],
        'hero_emoji': '🌿',
    },
    'jharsuguda': {
        'display_name': 'Jharsuguda',
        'tagline': 'The Powerhouse of Love',
        'romantic_desc': 'Industrial strength, natural beauty — Jharsuguda surprises you with waterfalls, rivers, and quiet romantic corners.',
        'state': 'Odisha',
        'places': ['Ib River', 'Belpahar Hills', 'Laxmi Narayan Temple', 'Brajrajnagar Industrial Area', 'Kolabira Forest'],
        'cafes': ['Café Coffee Day Jharsuguda', 'Hotel Arya Palace Restaurant', 'Sweet Shop Lane'],
        'activities': ['Ib River bank picnic', 'Hill drive to Belpahar', 'Temple visit at Laxmi Narayan', 'Drive through Kolabira forest'],
        'romantic_spots': ['Ib River sunset', 'Belpahar hilltop morning', 'Kolabira forest trail', 'Brajrajnagar evening walk'],
        'hotels': ['Hotel Arya Palace', 'Hotel Madhumita', 'Hotel Vrindavan'],
        'date_ideas': ['Ib River picnic', 'Belpahar hill sunrise drive', 'Temple visit + dinner'],
        'hero_emoji': '🏔️',
    },
    'jeypore': {
        'display_name': 'Jeypore',
        'tagline': 'The Tribal Heart Beats with Love',
        'romantic_desc': 'Deep in Koraput\'s valleys, Jeypore is where waterfalls, tribal markets, and untouched beauty make love feel like an adventure.',
        'state': 'Odisha',
        'places': ['Dudhari Waterfalls', 'Gupteswar Cave Temple', 'Hatipathar', 'Koraput Valley', 'Onkadelli Tribal Market'],
        'cafes': ['Hotel Hello Restaurant', 'Jeypore Sweets Corner', 'Local Adivasi food stalls', 'Koraput Café'],
        'activities': ['Waterfall trek to Dudhari', 'Visit Gupteswar Cave', 'Tribal market exploration', 'Drive through Koraput Valley'],
        'romantic_spots': ['Dudhari Waterfalls morning', 'Gupteswar Cave Temple sunset', 'Koraput Valley viewpoint', 'Hatipathar rock formations'],
        'hotels': ['Hotel Hello Jeypore', 'Hotel Nand Residency', 'Panthanivas Jeypore', 'Hotel Anam'],
        'date_ideas': ['Waterfall trek + picnic', 'Tribal market visit together', 'Valley drive at golden hour'],
        'hero_emoji': '🦋',
    },
    'koraput': {
        'display_name': 'Koraput',
        'tagline': 'Love in the Lap of Mountains',
        'romantic_desc': 'Mist-covered peaks, coffee plantations, and tribal soul — Koraput is Odisha\'s best-kept romantic secret.',
        'state': 'Odisha',
        'places': ['Tribal Museum', 'Dudhari Falls', 'Deomali Peak', 'Jagannath Sagar Lake', 'Sunabeda Wildlife Sanctuary'],
        'cafes': ['Panthanivas Restaurant', 'Hotel Trimurti', 'Koraput Coffee Corner', 'Local tribal eateries'],
        'activities': ['Trek to Deomali (highest peak of Odisha)', 'Coffee plantation visit', 'Tribal art exploration', 'Jagannath Sagar boating'],
        'romantic_spots': ['Deomali Peak sunrise', 'Jagannath Sagar Lake evening', 'Dudhari Falls misty morning', 'Sunabeda meadows'],
        'hotels': ['Panthanivas Koraput', 'Hotel Trimurti', 'Deomali Eco Resort', 'Government Rest House'],
        'date_ideas': ['Deomali Peak sunrise trek', 'Coffee tasting at local estate', 'Lake boating at Jagannath Sagar'],
        'hero_emoji': '🏔️',
    },
    'baripada': {
        'display_name': 'Baripada',
        'tagline': 'The Gateway to Wild Love',
        'romantic_desc': 'With Simlipal\'s tigers nearby and Mayurbhanj\'s heritage within reach, Baripada is romance wrapped in wilderness.',
        'state': 'Odisha',
        'places': ['Simlipal National Park', 'Haripur Palace', 'Khiching Temple', 'Devkund Waterfall', 'Joranda Falls'],
        'cafes': ['Hotel Ambika Restaurant', 'Janata Hotel', 'Baripada Sweets Market', 'Simlipal Restaurant'],
        'activities': ['Safari at Simlipal National Park', 'Waterfall trek to Joranda & Barehipani', 'Heritage tour of Haripur Palace', 'Forest walk'],
        'romantic_spots': ['Simlipal forest morning safari', 'Joranda Falls viewpoint', 'Barehipani Falls (tallest in Odisha)', 'Devkund Waterfall swim'],
        'hotels': ['Panthanivas Simlipal', 'Hotel Ambika', 'Simlipal Tiger Resort', 'Aranyak Nature Camp'],
        'date_ideas': ['Tiger safari at Simlipal', 'Waterfall picnic at Devkund', 'Palace heritage walk together'],
        'hero_emoji': '🐅',
    },
    'kendrapara': {
        'display_name': 'Kendrapara',
        'tagline': 'Where Nature Romances the River',
        'romantic_desc': 'Bhitarkanika mangroves, crocodile creeks, and river delta magic — Kendrapara is love at its most wild and free.',
        'state': 'Odisha',
        'places': ['Bhitarkanika National Park', 'Gahirmatha Beach (Olive Ridley)', 'Pentha Sea Beach', 'Hukitola Island', 'Tantidandapata'],
        'cafes': ['Panthanivas Restaurant', 'Local fish fry stalls', 'Kendrapara Sweets', 'Maa Hotel'],
        'activities': ['Boat safari at Bhitarkanika', 'Visit Olive Ridley nesting at Gahirmatha', 'Island hopping to Hukitola', 'Mangrove trail walk'],
        'romantic_spots': ['Bhitarkanika creek sunrise safari', 'Pentha Beach untouched shoreline', 'Hukitola Island sunset', 'White crocodile sighting'],
        'hotels': ['Panthanivas Dangmal', 'Bhitarkanika Nature Camp', 'Hotel Ganesh Kendrapara', 'Eco Cottages Bhitarkanika'],
        'date_ideas': ['Mangrove boat safari together', 'Beach day at Pentha', 'Hukitola island picnic'],
        'hero_emoji': '🐊',
    },
    'paradip': {
        'display_name': 'Paradip',
        'tagline': 'Love at the Port of Dreams',
        'romantic_desc': 'Where cargo ships sail out and love sails in — Paradip\'s beaches and port sunsets are unexpectedly romantic.',
        'state': 'Odisha',
        'places': ['Paradip Beach', 'Paradip Port', 'Marine Aquarium', 'Hukitola Mangrove Forest', 'Nehru Bungalow Park'],
        'cafes': ['Hotel Seagull Restaurant', 'Paradip Port Guest House Canteen', 'Beach shack stalls', 'Hotel Samrat Restaurant'],
        'activities': ['Beach walk at Paradip', 'Visit marine aquarium', 'Watch ships at the port', 'Fishing boat ride'],
        'romantic_spots': ['Paradip Beach sunset', 'Port area industrial sunset', 'Mangrove creek boating', 'Nehru Bungalow garden'],
        'hotels': ['Hotel Seagull', 'Hotel Samrat', 'Paradip Port Guest House', 'Hotel Millennium'],
        'date_ideas': ['Beach sunset walk', 'Aquarium visit + fish fry date', 'Ship-watching at the port'],
        'hero_emoji': '🚢',
    },
    'konark': {
        'display_name': 'Konark',
        'tagline': 'Love Carved in Stone',
        'romantic_desc': 'The Sun Temple knows — love is art, passion is eternal, and Konark is where both become one.',
        'state': 'Odisha',
        'places': ['Konark Sun Temple', 'Chandrabhaga Beach', 'ASI Museum', 'Ramachandi Temple', 'Konark Marine Drive'],
        'cafes': ['Panthanivas Restaurant', 'Lotus Eco Beach Resort Restaurant', 'Konark road-side dhabas', 'Beach shacks'],
        'activities': ['Explore Sun Temple carvings', 'Beach day at Chandrabhaga', 'Watch Konark dance festival (if Feb)', 'Marine drive evening'],
        'romantic_spots': ['Sun Temple at golden hour', 'Chandrabhaga Beach sunrise', 'Ramachandi beach bonfire', 'Marine drive road sunset'],
        'hotels': ['Lotus Eco Beach Resort', 'Panthanivas Konark', 'Yatri Nivas Konark', 'Hotel Sun Temple'],
        'date_ideas': ['Sun Temple sunrise visit', 'Chandrabhaga Beach picnic', 'Ramachandi beach bonfire dinner'],
        'hero_emoji': '☀️',
    },
    'dhenkanal': {
        'display_name': 'Dhenkanal',
        'tagline': 'A Love Hidden in Green Valleys',
        'romantic_desc': 'Waterfalls, sanctuaries, and old-world Odia charm — Dhenkanal is a romantic escape nobody told you about.',
        'state': 'Odisha',
        'places': ['Saptasajya Hills', 'Kapilash Temple', 'Dhenkanal Palace', 'Joranda Mahima Gaddi', 'Mahima Ashram'],
        'cafes': ['Hotel Annapurna', 'Dhenkanal Sweets Corner', 'Local chai stalls near palace', 'Maa Tarini Restaurant'],
        'activities': ['Trek to Saptasajya Hills', 'Visit Kapilash Temple', 'Explore Dhenkanal Palace', 'Drive through Kamakhyanagar forest'],
        'romantic_spots': ['Saptasajya Hills panoramic view', 'Kapilash Temple hilltop', 'Palace garden evening walk', 'Forest drive at dawn'],
        'hotels': ['Hotel Annapurna', 'Guest House Dhenkanal', 'Panthanivas Saptasajya', 'Budget hotels near bus stand'],
        'date_ideas': ['Hilltop trek to Saptasajya', 'Palace heritage walk', 'Forest drive + chai date'],
        'hero_emoji': '🌳',
    },
    'kendujhar': {
        'display_name': 'Kendujhar (Keonjhar)',
        'tagline': 'Iron Heart, Golden Love',
        'romantic_desc': 'Waterfalls cascading over red earth, dense forests, and the raw beauty of mineral-rich land — Keonjhar is untamed love.',
        'state': 'Odisha',
        'places': ['Sanaghagara Waterfall', 'Badaghagara Waterfall', 'Gonasika (Origin of Baitarani)', 'Sitabinji Rock Art', 'Bhimkund'],
        'cafes': ['Hotel Crystal Palace Restaurant', 'Keonjhar Sweets', 'Highway dhabas', 'Maa Hotel'],
        'activities': ['Waterfall hopping', 'Visit Gonasika sacred river origin', 'Rock art viewing at Sitabinji', 'Forest drive through Keonjhar'],
        'romantic_spots': ['Sanaghagara Falls misty morning', 'Gonasika sacred spring', 'Bhimkund reflection pool', 'Sitabinji cave paintings'],
        'hotels': ['Hotel Crystal Palace', 'Panthanivas Keonjhar', 'Hotel Mangalam', 'Eco Lodge Keonjhar'],
        'date_ideas': ['Waterfall trek + picnic', 'Gonasika sacred visit together', 'Forest drive at sunrise'],
        'hero_emoji': '💎',
    },
    'sundargarh': {
        'display_name': 'Sundargarh',
        'tagline': 'Love as Beautiful as Its Name',
        'romantic_desc': 'Named "beautiful land" — Sundargarh delivers with tribal culture, hidden waterfalls, and nature\'s purest romance.',
        'state': 'Odisha',
        'places': ['Mandira Dam', 'Ushabali Waterfall', 'Vedvyas Temple', 'Ghogar Hills', 'Tribal villages'],
        'cafes': ['Hotel Vaishnavi Restaurant', 'Sundargarh Sweets', 'Local dhabas', 'Tea stalls at bus stand'],
        'activities': ['Mandira Dam picnic', 'Tribal village visit', 'Waterfall trek to Ushabali', 'Hill drive to Ghogar'],
        'romantic_spots': ['Mandira Dam sunset', 'Ushabali Waterfall creek', 'Ghogar Hills viewpoint', 'Vedvyas riverbank'],
        'hotels': ['Hotel Vaishnavi', 'Panthanivas Sundargarh', 'Guest houses', 'Budget hotels'],
        'date_ideas': ['Dam picnic + sunset', 'Waterfall trek together', 'Tribal art shopping date'],
        'hero_emoji': '🌺',
    },
    'rayagada': {
        'display_name': 'Rayagada',
        'tagline': 'Love in the Land of Tribal Souls',
        'romantic_desc': 'Dongariya Kondh markets, misty valleys, and nature so raw it takes your breath away — Rayagada is love unplugged.',
        'state': 'Odisha',
        'places': ['Chatikona Tribal Market', 'Minajhola Waterfall', 'Devgiri Hills', 'Niyamgiri Hills', 'Laxminarayan Temple'],
        'cafes': ['Hotel Sai International Restaurant', 'Rayagada Sweets', 'Local tribal food stalls', 'Maa Tarini Hotel'],
        'activities': ['Tribal market visit at Chatikona', 'Waterfall trek to Minajhola', 'Niyamgiri Hills exploration', 'Tribal art and craft tour'],
        'romantic_spots': ['Niyamgiri Hills sunrise', 'Minajhola Falls misty morning', 'Chatikona market colors', 'Devgiri hilltop view'],
        'hotels': ['Hotel Sai International', 'Hotel Tejasree', 'Panthanivas Rayagada', 'Budget guest houses'],
        'date_ideas': ['Tribal market exploration', 'Niyamgiri sunrise trek', 'Waterfall picnic at Minajhola'],
        'hero_emoji': '🎨',
    },
    'jajpur': {
        'display_name': 'Jajpur',
        'tagline': 'Ancient Love on Sacred Shores',
        'romantic_desc': 'The ancient capital of Odisha — where Baitarani River flows with devotion and every temple tells a love story from centuries past.',
        'state': 'Odisha',
        'places': ['Biraja Temple', 'Ratnagiri Buddhist Ruins', 'Udayagiri (Jajpur)', 'Lalitgiri', 'Baitarani River Ghat'],
        'cafes': ['Jajpur Road station area eateries', 'Biraja Temple prasad stall', 'Local sweets shops', 'Highway dhabas'],
        'activities': ['Buddhist triangle tour (Ratnagiri-Udayagiri-Lalitgiri)', 'Temple heritage walk', 'Baitarani River evening', 'Museum visit at Ratnagiri'],
        'romantic_spots': ['Ratnagiri monastery at sunset', 'Baitarani River sacred ghat', 'Lalitgiri hilltop viewpoint', 'Biraja Temple garden'],
        'hotels': ['Hotels near Jajpur Road', 'Guest houses at Ratnagiri', 'Panthanivas', 'Budget stays at Jajpur town'],
        'date_ideas': ['Buddhist heritage trail together', 'Riverside walk at Baitarani', 'Temple visit + local sweets'],
        'hero_emoji': '🛕',
    },
    'kalahandi': {
        'display_name': 'Kalahandi (Bhawanipatna)',
        'tagline': 'Wild Love in Untamed Forests',
        'romantic_desc': 'Deep gorges, ancient caves, and tribal heritage — Kalahandi is where love feels like a jungle adventure.',
        'state': 'Odisha',
        'places': ['Phurlijharan Waterfall', 'Karlapat Wildlife Sanctuary', 'Gudahandi Rock Edicts', 'Ampani', 'Thuamul Rampur'],
        'cafes': ['Hotel Rajdhani Restaurant', 'Bhawanipatna Sweets', 'Local eateries', 'Highway stops'],
        'activities': ['Waterfall trek to Phurlijharan', 'Wildlife safari at Karlapat', 'Cave exploration at Gudahandi', 'Drive through Thuamul Rampur'],
        'romantic_spots': ['Phurlijharan Falls morning', 'Karlapat forest sunrise', 'Gudahandi ancient carvings at sunset', 'Ampani valley view'],
        'hotels': ['Hotel Rajdhani', 'Panthanivas Bhawanipatna', 'Government Guest House', 'Budget hotels'],
        'date_ideas': ['Waterfall trek + picnic', 'Jungle safari together', 'Rock art exploration date'],
        'hero_emoji': '🦚',
    },
    'bolangir': {
        'display_name': 'Bolangir',
        'tagline': 'Love Written in Ancient Walls',
        'romantic_desc': 'Temple carvings, quiet rivers, and the slow charm of western Odisha — Bolangir is romance at a gentle pace.',
        'state': 'Odisha',
        'places': ['Harishankar Temple', 'Ranipur Jharial', 'Patneswari Temple', 'Gandhamardan Hills'],
        'cafes': ['Hotel Pushpak Restaurant', 'Local sweets shops', 'Bolangir Chaat Street', 'Highway dhabas'],
        'activities': ['Trek to Harishankar waterfalls', 'Explore Ranipur Jharial ancient ruins', 'Drive through Gandhamardan Hills', 'Temple trail'],
        'romantic_spots': ['Harishankar Temple waterfall', 'Ranipur Jharial ruins at golden hour', 'Gandhamardan hilltop', 'Patneswari Temple garden'],
        'hotels': ['Hotel Pushpak', 'Hotel Raj', 'Government Guest House', 'Budget hotels'],
        'date_ideas': ['Harishankar waterfall picnic', 'Ancient ruins exploration', 'Hill drive at sunset'],
        'hero_emoji': '🏚️',
    },
    'mayurbhanj': {
        'display_name': 'Mayurbhanj',
        'tagline': 'Royal Forests, Wild Love',
        'romantic_desc': 'Simlipal\'s waterfalls, tribal art, and palace ruins — Mayurbhanj is where love goes on an untamed adventure.',
        'state': 'Odisha',
        'places': ['Simlipal National Park', 'Barehipani Falls', 'Joranda Falls', 'Haripur Palace', 'Khiching Temple'],
        'cafes': ['Simlipal canteen', 'Baripada local eateries', 'Palace road food stalls', 'Panthanivas restaurant'],
        'activities': ['Simlipal jungle safari', 'Waterfall trekking', 'Tribal craft tour', 'Heritage palace visit'],
        'romantic_spots': ['Barehipani Falls viewpoint', 'Simlipal core forest morning', 'Joranda Falls mist', 'Haripur Palace sunset'],
        'hotels': ['Panthanivas Simlipal', 'Aranyak Nature Camp', 'Hotel Ambika Baripada', 'Simlipal Tiger Resort'],
        'date_ideas': ['Tiger safari adventure', 'Waterfall trek in Simlipal', 'Tribal market date'],
        'hero_emoji': '🐆',
    },
    'nayagarh': {
        'display_name': 'Nayagarh',
        'tagline': 'Love in the Lap of Hidden Forests',
        'romantic_desc': 'Community forests, quiet dams, and the magic of Odisha\'s green heartland — Nayagarh is a hidden romantic gem.',
        'state': 'Odisha',
        'places': ['Belghar Wildlife Sanctuary', 'Khandadhar Waterfalls', 'Odagaon', 'Dasapalla Palace', 'Ranpur Forest'],
        'cafes': ['Local restaurants in Nayagarh town', 'Highway dhabas', 'Sweet shops near bus stand'],
        'activities': ['Wildlife viewing at Belghar', 'Waterfall trek', 'Dasapalla Palace heritage visit', 'Forest drive'],
        'romantic_spots': ['Khandadhar Falls morning', 'Belghar forest trail', 'Dasapalla Palace ruins', 'Forest canopy walk'],
        'hotels': ['Government Rest House', 'Budget hotels in Nayagarh town', 'Eco stays near Belghar', 'Panthanivas'],
        'date_ideas': ['Forest walk + picnic', 'Waterfall trek together', 'Palace heritage date'],
        'hero_emoji': '🌲',
    },
    'jagatsinghpur': {
        'display_name': 'Jagatsinghpur',
        'tagline': 'Love Where the River Meets the Sea',
        'romantic_desc': 'Mahanadi delta, Paradip shores, and the spiritual energy of Sarala Pitha — love flows naturally here.',
        'state': 'Odisha',
        'places': ['Sarala Temple', 'Paradip Port & Beach', 'Kujang', 'Machhagaon', 'Taladanda Canal'],
        'cafes': ['Local restaurants', 'Fish fry stalls near Paradip', 'Jagatsinghpur town eateries'],
        'activities': ['Beach visit at Paradip', 'Sarala Temple trail', 'Canal-side walk at Taladanda', 'Fish market exploration'],
        'romantic_spots': ['Paradip Beach sunset', 'Taladanda Canal evening', 'Sarala Temple morning', 'Delta river banks'],
        'hotels': ['Hotels at Paradip', 'Guest houses in Jagatsinghpur', 'Panthanivas', 'Budget stays'],
        'date_ideas': ['Beach day at Paradip', 'Temple visit + seafood dinner', 'Canal walk at sunset'],
        'hero_emoji': '⛵',
    },
    'sonepur': {
        'display_name': 'Sonepur (Subarnapur)',
        'tagline': 'Golden Love by the River',
        'romantic_desc': 'Named after gold, kissed by the Tel River — Sonepur is where love shines as warm as its name.',
        'state': 'Odisha',
        'places': ['Subarnameru Temple', 'Tel River Ghat', 'Cotton Textile Market', 'Rampur Palace', 'Birupa River'],
        'cafes': ['Local restaurants', 'Sweet shops at main road', 'Tea stalls near temple'],
        'activities': ['River bank walk at Tel', 'Temple visit at Subarnameru', 'Cotton saree shopping', 'Heritage walk'],
        'romantic_spots': ['Tel River sunset', 'Subarnameru Temple morning', 'Cotton weaving village visit', 'River bank picnic'],
        'hotels': ['Government Guest House', 'Budget hotels', 'Dharamshalas near temple'],
        'date_ideas': ['Riverside picnic', 'Cotton saree shopping together', 'Temple visit at dawn'],
        'hero_emoji': '✨',
    },
    'bargarh': {
        'display_name': 'Bargarh',
        'tagline': 'Dhanu Jatra and Love Stories',
        'romantic_desc': 'Famous for the world\'s largest open-air theater (Dhanu Jatra) — Bargarh turns love into a spectacle.',
        'state': 'Odisha',
        'places': ['Nrusinghanath Temple', 'Pabitra Mohan Temple', 'Papanga Hills', 'Gandhamardan Hills', 'Ambabhona Waterfall'],
        'cafes': ['Hotel Sagar Restaurant', 'Local sweet shops', 'Bargarh Chaat Market', 'Highway dhabas'],
        'activities': ['Temple trek to Nrusinghanath', 'Hill drive to Papanga', 'Gandhamardan herbal trail', 'Local market exploration'],
        'romantic_spots': ['Nrusinghanath Temple waterfall', 'Papanga Hills sunrise', 'Gandhamardan forest walk', 'Ambabhona waterfalls'],
        'hotels': ['Hotel Sagar', 'Government Guest House', 'Budget hotels near bus stand'],
        'date_ideas': ['Hill temple trek together', 'Gandhamardan herbal walk', 'Waterfall picnic'],
        'hero_emoji': '🎭',
    },
    'nuapada': {
        'display_name': 'Nuapada',
        'tagline': 'Simple Love in Simple Lanes',
        'romantic_desc': 'No fancy lights, just stars. No noise, just heartbeats. Nuapada is love stripped to its purest, most beautiful form.',
        'state': 'Odisha',
        'places': ['Patora Fort', 'Sunabeda Wildlife Sanctuary', 'Yogimatha Cave', 'Budhikomna', 'Boden Dam'],
        'cafes': ['Local eateries at Nuapada town', 'Tea stalls', 'Highway food joints'],
        'activities': ['Fort exploration at Patora', 'Wildlife walk at Sunabeda', 'Cave visit at Yogimatha', 'Dam picnic at Boden'],
        'romantic_spots': ['Sunabeda plateau sunrise', 'Boden Dam sunset', 'Yogimatha Cave entry', 'Patora Fort hilltop'],
        'hotels': ['Government Guest House', 'Budget hotels', 'Rest houses near Sunabeda'],
        'date_ideas': ['Plateau sunrise at Sunabeda', 'Dam picnic at Boden', 'Fort exploration together'],
        'hero_emoji': '🌌',
    },
    'malkangiri': {
        'display_name': 'Malkangiri',
        'tagline': 'Love at the Edge of the World',
        'romantic_desc': 'Odisha\'s remotest corner — where Chitrakonda reservoir sparkles and tribal heartbeats sync with yours.',
        'state': 'Odisha',
        'places': ['Chitrakonda Dam', 'Mudulipada', 'Satiguda Dam', 'Balimela Reservoir', 'Motu (Tri-junction point)'],
        'cafes': ['Local restaurants', 'Tribal food experiences', 'Government canteens', 'Highway stops'],
        'activities': ['Boating at Chitrakonda', 'Visit tribal villages', 'Explore Balimela Reservoir', 'Drive to tri-junction point'],
        'romantic_spots': ['Chitrakonda Reservoir sunset', 'Balimela Dam morning', 'Satiguda Lake reflections', 'Motu tri-junction view'],
        'hotels': ['Panthanivas Malkangiri', 'Government Rest House', 'Budget hotels'],
        'date_ideas': ['Reservoir boating at Chitrakonda', 'Tribal village art walk', 'Tri-junction border visit'],
        'hero_emoji': '🗺️',
    },
    'nabarangpur': {
        'display_name': 'Nabarangpur',
        'tagline': 'Where Innocence Falls in Love',
        'romantic_desc': 'Tribal innocence, ancient traditions, and nature untouched — Nabarangpur is love without filters.',
        'state': 'Odisha',
        'places': ['Bhairabsingpur', 'Ancient Cave Paintings', 'Kolkundi Waterfalls', 'Turi Buru Hills', 'Jharigaon'],
        'cafes': ['Local restaurants', 'Street food at bus stand', 'Highway dhabas'],
        'activities': ['Cave painting exploration', 'Waterfall trek', 'Tribal market visit', 'Hill drive to Turi Buru'],
        'romantic_spots': ['Kolkundi Waterfalls morning', 'Turi Buru hilltop', 'Ancient cave art site', 'Jharigaon countryside'],
        'hotels': ['Government Guest House', 'Budget hotels', 'Rest houses'],
        'date_ideas': ['Cave art exploration date', 'Waterfall trek + picnic', 'Hill drive together'],
        'hero_emoji': '🎪',
    },
    'gajapati': {
        'display_name': 'Gajapati (Paralakhemundi)',
        'tagline': 'Mountain Love in Eastern Ghats',
        'romantic_desc': 'Eastern Ghats\' finest — where Mahendragiri\'s peak touches the clouds and your love touches infinity.',
        'state': 'Odisha',
        'places': ['Mahendragiri Peak', 'Baranga Wildlife Sanctuary', 'Taratarini (nearby)', 'Paralakhemundi Palace', 'Gumma Hill'],
        'cafes': ['Local eateries in Paralakhemundi', 'Highway stops', 'Sweet shops'],
        'activities': ['Trek to Mahendragiri Peak', 'Wildlife at Baranga', 'Palace visit', 'Gumma Hill drive'],
        'romantic_spots': ['Mahendragiri sunrise', 'Baranga forest trail', 'Palace garden evening', 'Gumma Hill viewpoint'],
        'hotels': ['Rest houses', 'Budget hotels at Paralakhemundi', 'Forest lodges'],
        'date_ideas': ['Mahendragiri sunrise trek', 'Forest safari at Baranga', 'Palace heritage walk'],
        'hero_emoji': '⛰️',
    },
    'kandhamal': {
        'display_name': 'Kandhamal (Phulbani)',
        'tagline': 'Spice of Love, Sweetness of Turmeric',
        'romantic_desc': 'Turmeric fields, hill streams, and Kondh tribal art — Kandhamal is where love has the most beautiful earthy aroma.',
        'state': 'Odisha',
        'places': ['Daringbadi (Kashmir of Odisha)', 'Putudi Waterfall', 'Mandasaru Dam', 'Coffee & Pepper plantations', 'Belghar Sanctuary'],
        'cafes': ['Daringbadi resort restaurants', 'Local food in Phulbani', 'Coffee plantation tastings'],
        'activities': ['Valley walk at Daringbadi', 'Waterfall visit at Putudi', 'Coffee plantation tour', 'Dam visit at Mandasaru'],
        'romantic_spots': ['Daringbadi hill station morning mist', 'Putudi Waterfall picnic', 'Coffee plantation walk', 'Mandasaru Dam sunset'],
        'hotels': ['Daringbadi Nature Camp', 'Panthanivas Daringbadi', 'Hill View Resort', 'Budget stays in Phulbani'],
        'date_ideas': ['Daringbadi misty walk', 'Coffee plantation date', 'Waterfall picnic at Putudi'],
        'hero_emoji': '🌶️',
    },
    'daringbadi': {
        'display_name': 'Daringbadi',
        'tagline': 'The Kashmir of Odisha — Where Love Blooms in Mist',
        'romantic_desc': 'Pine forests, coffee plantations, and cool misty mornings — Daringbadi is Odisha\'s most romantic hill station.',
        'state': 'Odisha',
        'places': ['Hill View Point', 'Lover\'s Point', 'Coffee Garden', 'Daringbadi Nature Camp', 'Mandasaru Dam', 'Putudi Waterfall'],
        'cafes': ['Nature Camp Restaurant', 'Hill View Cafe', 'Coffee plantation tasting', 'Local food stalls'],
        'activities': ['Misty morning walk at Lover\'s Point', 'Coffee plantation tour', 'Pine forest trek', 'Waterfall visit'],
        'romantic_spots': ['Lover\'s Point sunrise', 'Pine forest misty trail', 'Coffee Garden morning', 'Hill View sunset'],
        'hotels': ['Daringbadi Nature Camp', 'Panthanivas Daringbadi', 'Hill View Resort', 'Pine Forest Resort'],
        'date_ideas': ['Sunrise at Lover\'s Point', 'Coffee tasting walk', 'Pine forest trek together'],
        'hero_emoji': '🌲',
    },

    # ==================== MAJOR METRO CITIES ====================
    'delhi': {
        'display_name': 'Delhi',
        'tagline': 'Where Every Lane Tells a Love Story',
        'romantic_desc': 'From Mughal gardens to rooftop cafes, Delhi wraps every couple in history, culture, and magic.',
        'state': 'Delhi',
        'places': ['India Gate', 'Lodhi Garden', 'Hauz Khas Village', 'Connaught Place', 'Lotus Temple'],
        'cafes': ['Cafe Lota', 'The Blue Door Cafe', 'Kunzum Travel Cafe', 'Cha Bar', 'Rose Cafe'],
        'activities': ['Sunset at India Gate', 'Street food at Chandni Chowk', 'Art galleries in Hauz Khas'],
        'romantic_spots': ['Lodhi Garden at dawn', 'Humayun\'s Tomb sunset', 'Hauz Khas Lake evening', 'Agrasen ki Baoli'],
        'hotels': ['The Imperial', 'Taj Palace', 'The Leela Palace', 'ITC Maurya'],
        'date_ideas': ['Heritage walk through Old Delhi', 'Rooftop dinner at Hauz Khas', 'Boating at Purana Qila lake'],
        'hero_emoji': '🕌',
    },
    'mumbai': {
        'display_name': 'Mumbai',
        'tagline': 'The City That Never Stops Loving',
        'romantic_desc': 'Sea breeze at Marine Drive, stolen glances at Gateway — Mumbai is where love feels cinematic.',
        'state': 'Maharashtra',
        'places': ['Marine Drive', 'Gateway of India', 'Bandra Fort', 'Juhu Beach', 'Worli Sea Face'],
        'cafes': ['Prithvi Cafe', 'Leopold Cafe', 'Candies', 'The Pantry', 'Cafe Mondegar'],
        'activities': ['Evening at Marine Drive', 'Ferry ride to Elephanta Caves', 'Street food at Mohammed Ali Road'],
        'romantic_spots': ['Marine Drive at midnight', 'Bandstand promenade sunset', 'Worli Sea Link golden hour', 'Carter Road walk'],
        'hotels': ['Taj Mahal Palace', 'The Oberoi', 'Trident Nariman Point', 'ITC Grand Central'],
        'date_ideas': ['Sunset ferry to Mandwa', 'Candlelight at Dome rooftop', 'Bandra Fort stargazing'],
        'hero_emoji': '🌊',
    },
    'bangalore': {
        'display_name': 'Bangalore',
        'tagline': 'Love Brews Here',
        'romantic_desc': 'Cool weather, cozy cafes, and garden city vibes — Bangalore makes every date feel like a movie.',
        'state': 'Karnataka',
        'places': ['Lalbagh Botanical Garden', 'Cubbon Park', 'Ulsoor Lake', 'Wonderla', 'Nandi Hills'],
        'cafes': ['The Hole in the Wall', 'Koshy\'s', 'Third Wave Coffee', 'The Egg Factory', 'Cafe Azzure'],
        'activities': ['Early morning trip to Nandi Hills', 'Pub hopping on MG Road', 'Shopping on Commercial Street'],
        'romantic_spots': ['Nandi Hills sunrise', 'Lalbagh glasshouse evening', 'Sankey Tank sunset', 'Cubbon Park rain walk'],
        'hotels': ['The Leela Palace', 'Taj West End', 'ITC Windsor', 'Shangri-La'],
        'date_ideas': ['Sunrise drive to Nandi Hills', 'Wine tasting in Sula vineyards', 'Breakfast at Koshy\'s'],
        'hero_emoji': '☕',
    },
    'kolkata': {
        'display_name': 'Kolkata',
        'tagline': 'The City of Joy & Love',
        'romantic_desc': 'Trams, Tagore, and tender moments — Kolkata loves you back in the most poetic way.',
        'state': 'West Bengal',
        'places': ['Victoria Memorial', 'Howrah Bridge', 'Prinsep Ghat', 'Park Street', 'Dakshineswar Temple'],
        'cafes': ['Flurys', 'Indian Coffee House', 'Cafe Mezzuna', 'The Corner Courtyard', 'Mrs. Magpie'],
        'activities': ['Evening boat ride on Hooghly', 'Book shopping at College Street', 'Tram ride through the city'],
        'romantic_spots': ['Prinsep Ghat at sunset', 'Victoria Memorial night lights', 'Eco Park boating', 'Marble Palace afternoon'],
        'hotels': ['The Oberoi Grand', 'Taj Bengal', 'ITC Royal Bengal', 'The Park Kolkata'],
        'date_ideas': ['Tram ride + chai date', 'Sunset at Prinsep Ghat', 'Candlelight at 6 Ballygunge Place'],
        'hero_emoji': '🎭',
    },
    'jaipur': {
        'display_name': 'Jaipur',
        'tagline': 'The Pink City of Royal Romance',
        'romantic_desc': 'Palaces painted in love, forts that guard forever stories — Jaipur is romance written in stone.',
        'state': 'Rajasthan',
        'places': ['Hawa Mahal', 'Amer Fort', 'Nahargarh Fort', 'City Palace', 'Jal Mahal'],
        'cafes': ['Tapri Central', 'Curious Life Coffee Roasters', 'Bar Palladio', 'Cafe Bae'],
        'activities': ['Hot air balloon ride', 'Elephant ride at Amer Fort', 'Shopping at Johari Bazaar'],
        'romantic_spots': ['Nahargarh Fort sunset', 'Jal Mahal evening view', 'Amer Fort light show', 'Patrika Gate golden hour'],
        'hotels': ['Rambagh Palace', 'Taj Jai Mahal Palace', 'The Oberoi Rajvilas', 'Fairmont Jaipur'],
        'date_ideas': ['Sunset dinner at Nahargarh', 'Palace walk at Amer', 'Elephant ride together'],
        'hero_emoji': '🏰',
    },
    'goa': {
        'display_name': 'Goa',
        'tagline': 'Where the Ocean Sings Love Songs',
        'romantic_desc': 'Sandy toes, salty kisses, golden sunsets — Goa is where love dances barefoot.',
        'state': 'Goa',
        'places': ['Baga Beach', 'Fort Aguada', 'Chapora Fort', 'Dudhsagar Falls', 'Old Goa Churches'],
        'cafes': ['Artjuna', 'Burger Factory', 'Cafe Bodega', 'The Fisherman\'s Wharf'],
        'activities': ['Sunset cruise on Mandovi River', 'Scuba diving', 'Beach shack dinner'],
        'romantic_spots': ['Palolem Beach sunset', 'Chapora Fort sunrise', 'Butterfly Beach hidden cove', 'Divar Island'],
        'hotels': ['Taj Exotica', 'The Leela Goa', 'W Goa', 'Alila Diwa'],
        'date_ideas': ['Sunset cruise + dinner', 'Private beach picnic', 'Couple\'s spa at Taj Exotica'],
        'hero_emoji': '🏖️',
    },
    'udaipur': {
        'display_name': 'Udaipur',
        'tagline': 'The Venice of the East',
        'romantic_desc': 'Lake palaces, floating candlelight, royal sunsets — Udaipur is a love letter you can walk through.',
        'state': 'Rajasthan',
        'places': ['Lake Pichola', 'City Palace', 'Jag Mandir', 'Saheliyon Ki Bari', 'Monsoon Palace'],
        'cafes': ['Cafe Edelweiss', 'Jheel Cafe', 'Charcoal by Carlsson', 'Savage Garden'],
        'activities': ['Boat ride on Lake Pichola', 'Puppet show at Bagore Ki Haveli', 'Rooftop dinner with lake view'],
        'romantic_spots': ['Lake Pichola sunset boat', 'Monsoon Palace evening', 'Ambrai Ghat lake view', 'Jag Mandir island'],
        'hotels': ['Taj Lake Palace', 'The Oberoi Udaivilas', 'The Leela Palace', 'Fateh Prakash Palace'],
        'date_ideas': ['Candlelight dinner at Jag Mandir', 'Sunrise at Monsoon Palace', 'Boating under stars'],
        'hero_emoji': '🏯',
    },

    # ==================== MORE TOP INDIAN CITIES ====================
    'hyderabad': {
        'display_name': 'Hyderabad',
        'tagline': 'The City of Pearls & Passion',
        'romantic_desc': 'Biryani, Charminar, and Hussain Sagar sunsets — Hyderabad is where Nizami romance still lives in every lane.',
        'state': 'Telangana',
        'places': ['Charminar', 'Hussain Sagar Lake', 'Golconda Fort', 'Ramoji Film City', 'Salar Jung Museum'],
        'cafes': ['Roastery Coffee House', 'Autumn Leaf Cafe', 'Concu', 'Kaficko', 'Feranoz Patisserie'],
        'activities': ['Boating at Hussain Sagar', 'Sound & light show at Golconda Fort', 'Old city food walk'],
        'romantic_spots': ['Hussain Sagar sunset boat ride', 'Golconda Fort evening', 'Necklace Road night walk', 'Durgam Cheruvu lakefront'],
        'hotels': ['Taj Falaknuma Palace', 'ITC Kohenur', 'Park Hyatt', 'Novotel HICC'],
        'date_ideas': ['Royal dinner at Falaknuma Palace', 'Boating at Hussain Sagar', 'Old city biryani trail'],
        'hero_emoji': '💎',
    },
    'chennai': {
        'display_name': 'Chennai',
        'tagline': 'Where the Bay Whispers Love',
        'romantic_desc': 'Marina Beach mornings, filter coffee evenings, and temple town warmth — Chennai is love with a South Indian soul.',
        'state': 'Tamil Nadu',
        'places': ['Marina Beach', 'Kapaleeshwarar Temple', 'San Thome Cathedral', 'Elliot\'s Beach', 'Mahabalipuram (nearby)'],
        'cafes': ['Amethyst', 'Chamiers Cafe', 'Writer\'s Cafe', 'Sandy\'s Chocolate Laboratory', 'The Brew Room'],
        'activities': ['Sunrise at Marina Beach', 'Art walk at Cholamandal Village', 'Mahabalipuram day trip'],
        'romantic_spots': ['Elliot\'s Beach sunset', 'Marina Beach sunrise walk', 'Broken Bridge (Adyar River)', 'Covelong Beach'],
        'hotels': ['ITC Grand Chola', 'Taj Connemara', 'The Park Chennai', 'Leela Palace Chennai'],
        'date_ideas': ['Sunrise at Marina + filter coffee', 'Art village walk at Cholamandal', 'Mahabalipuram heritage trip'],
        'hero_emoji': '🌅',
    },
    'pune': {
        'display_name': 'Pune',
        'tagline': 'Oxford of Love Stories',
        'romantic_desc': 'College memories, hill fort treks, and Koregaon Park cafe culture — Pune is where young love finds its rhythm.',
        'state': 'Maharashtra',
        'places': ['Shaniwar Wada', 'Sinhagad Fort', 'Aga Khan Palace', 'Pashan Lake', 'Lavasa (nearby)'],
        'cafes': ['Vohuman Cafe', 'Cafe Durga', 'The French Window', 'Pagdandi Bookstore Cafe', 'Fleur Patisserie'],
        'activities': ['Sinhagad Fort sunrise trek', 'Cafe hopping in Koregaon Park', 'Day trip to Lavasa'],
        'romantic_spots': ['Sinhagad Fort sunrise', 'Pashan Lake evening', 'Okayama Garden sunset', 'Mulshi Dam backwaters'],
        'hotels': ['JW Marriott', 'The Ritz-Carlton', 'Conrad Pune', 'Hyatt Pune'],
        'date_ideas': ['Sinhagad sunrise trek + misal pav breakfast', 'Koregaon Park cafe trail', 'Mulshi Dam drive'],
        'hero_emoji': '🎓',
    },
    'ahmedabad': {
        'display_name': 'Ahmedabad',
        'tagline': 'Heritage Heart, Loving Soul',
        'romantic_desc': 'Pol houses, Sabarmati riverfront, and the sweetness of Gujarati hospitality — Ahmedabad loves quietly but deeply.',
        'state': 'Gujarat',
        'places': ['Sabarmati Riverfront', 'Adalaj Stepwell', 'Kankaria Lake', 'Jama Masjid', 'Science City'],
        'cafes': ['Manek Chowk (night food market)', 'The Green House', 'Cafe Upper Crust', 'Zen Cafe', 'Mocha Cafe'],
        'activities': ['Evening at Sabarmati Riverfront', 'Heritage pol walk in old city', 'Kankaria Lake amusement'],
        'romantic_spots': ['Sabarmati Riverfront sunset', 'Adalaj Stepwell morning light', 'Kankaria Lake evening ride', 'Law Garden night market'],
        'hotels': ['Hyatt Regency', 'Taj Skyline', 'ITC Narmada', 'Courtyard by Marriott'],
        'date_ideas': ['Heritage pol walk + street food', 'Sabarmati Riverfront dinner', 'Kankaria Lake joy ride'],
        'hero_emoji': '🪔',
    },
    'lucknow': {
        'display_name': 'Lucknow',
        'tagline': 'The City of Tehzeeb & Timeless Love',
        'romantic_desc': 'Nawabi elegance, kebab trails, and the most poetic Urdu whispered under moonlit monuments — Lucknow is love with adab.',
        'state': 'Uttar Pradesh',
        'places': ['Bara Imambara', 'Rumi Darwaza', 'British Residency', 'Hazratganj', 'Ambedkar Memorial Park'],
        'cafes': ['Royal Cafe (basket chaat!)', 'Sharma Ji Ki Chai', 'The Vintage Machine', 'Cappuccino Blast', 'Cafe De Lucknow'],
        'activities': ['Heritage walk through old Lucknow', 'Kebab trail (Tunday + Idris)', 'Shopping at Hazratganj'],
        'romantic_spots': ['Rumi Darwaza at twilight', 'Bara Imambara moonlit walk', 'Gomti Riverfront evening', 'British Residency sunset'],
        'hotels': ['Taj Mahal Lucknow', 'The Piccadily', 'Hyatt Regency', 'Lebua Lucknow'],
        'date_ideas': ['Tunday kebab trail together', 'Moonlit walk at Bara Imambara', 'Chikan shopping + chai date'],
        'hero_emoji': '🕌',
    },
    'chandigarh': {
        'display_name': 'Chandigarh',
        'tagline': 'The City Beautiful, The Love Wonderful',
        'romantic_desc': 'Clean roads, Sukhna Lake breezes, and Rock Garden whimsy — Chandigarh is love designed to perfection.',
        'state': 'Chandigarh',
        'places': ['Sukhna Lake', 'Rock Garden', 'Rose Garden', 'Elante Mall', 'Capitol Complex'],
        'cafes': ['The Brew Estate', 'Backpackers Cafe', 'Nik Baker\'s', 'Cafe JC\'s', 'The Willow Cafe'],
        'activities': ['Boating at Sukhna Lake', 'Cycling around Sector 17', 'Rock Garden exploration'],
        'romantic_spots': ['Sukhna Lake sunrise', 'Rose Garden morning walk', 'Sector 17 evening stroll', 'Timber Trail (nearby)'],
        'hotels': ['Taj Chandigarh', 'JW Marriott', 'The Lalit', 'Hyatt Regency'],
        'date_ideas': ['Sukhna Lake sunrise + breakfast', 'Rose Garden stroll', 'Timber Trail cable car trip'],
        'hero_emoji': '🌹',
    },
    'shimla': {
        'display_name': 'Shimla',
        'tagline': 'Where Snowflakes Write Love Letters',
        'romantic_desc': 'Colonial charm, misty mornings, and Mall Road magic — Shimla is the classic Indian honeymoon dream.',
        'state': 'Himachal Pradesh',
        'places': ['Mall Road', 'Ridge', 'Jakhoo Temple', 'Christ Church', 'Kufri'],
        'cafes': ['Wake & Bake', 'Cafe Simla Times', 'Indian Coffee House', 'AMA Cafe', 'Hide Out Cafe'],
        'activities': ['Walk on Mall Road', 'Toy train ride to Kalka', 'Ice skating (winter)'],
        'romantic_spots': ['Ridge at sunset', 'Scandal Point evening', 'Jakhoo Temple hilltop view', 'Kufri snow point'],
        'hotels': ['Wildflower Hall (Oberoi)', 'Cecil (Oberoi)', 'Clarkes Hotel', 'Radisson Shimla'],
        'date_ideas': ['Toy train ride together', 'Snow walk at Kufri', 'Candlelight dinner at Cecil'],
        'hero_emoji': '❄️',
    },
    'manali': {
        'display_name': 'Manali',
        'tagline': 'Mountains, Music & Moonlight Love',
        'romantic_desc': 'Snow-capped peaks, Beas River whispers, and cozy cafe nights — Manali is where love wears a warm jacket.',
        'state': 'Himachal Pradesh',
        'places': ['Solang Valley', 'Rohtang Pass', 'Hadimba Temple', 'Old Manali', 'Beas River'],
        'cafes': ['Lazy Dog Lounge', 'Drifters\' Cafe', 'Johnson\'s Cafe', 'Il Forno', 'Renaissance Cafe'],
        'activities': ['Snow activities at Solang Valley', 'River rafting on Beas', 'Cafe hopping in Old Manali'],
        'romantic_spots': ['Solang Valley snow morning', 'Old Manali evening cafes', 'Beas River bank sunset', 'Jogini Waterfall trek'],
        'hotels': ['The Himalayan', 'Manu Allaya Resort', 'Solang Valley Resort', 'Johnson Lodge'],
        'date_ideas': ['Snow day at Solang Valley', 'Riverside bonfire + dinner', 'Jogini Waterfall trek together'],
        'hero_emoji': '🏔️',
    },
    'rishikesh': {
        'display_name': 'Rishikesh',
        'tagline': 'Adventure, Aarti & Aashiqui',
        'romantic_desc': 'Ganga aarti, cliff jumping, and Beatles ashram vibes — Rishikesh is where love goes on a spiritual adventure.',
        'state': 'Uttarakhand',
        'places': ['Laxman Jhula', 'Ram Jhula', 'Triveni Ghat', 'Beatles Ashram', 'Neer Garh Waterfall'],
        'cafes': ['Little Buddha Cafe', 'The Sitting Elephant', 'Beatles Cafe', 'Freedom Cafe', 'Cafe De Goa'],
        'activities': ['River rafting on Ganga', 'Bungee jumping', 'Ganga Aarti at Triveni Ghat'],
        'romantic_spots': ['Laxman Jhula sunset', 'Ganga riverside morning yoga', 'Beatles Ashram art walls', 'Neer Garh Waterfall swim'],
        'hotels': ['Aloha on the Ganges', 'Atali Ganga', 'The Roseate Ganges', 'JW Marriott Mussoorie (nearby)'],
        'date_ideas': ['River rafting + cliff jumping', 'Ganga Aarti date at sunset', 'Beatles Ashram art walk'],
        'hero_emoji': '🧘',
    },
    'agra': {
        'display_name': 'Agra',
        'tagline': 'The City Where Love Became Immortal',
        'romantic_desc': 'The Taj Mahal — the greatest love story ever built. Agra is where love becomes eternal, literally carved in marble.',
        'state': 'Uttar Pradesh',
        'places': ['Taj Mahal', 'Agra Fort', 'Mehtab Bagh', 'Fatehpur Sikri', 'Itmad-ud-Daulah'],
        'cafes': ['Cafe Sheroes Hangout', 'Bon Barbecue', 'Pinch of Spice', 'Mama Chicken', 'Esphahan (The Oberoi)'],
        'activities': ['Sunrise at Taj Mahal', 'Sunset from Mehtab Bagh', 'Marble inlay art workshop'],
        'romantic_spots': ['Taj Mahal at sunrise', 'Mehtab Bagh sunset view of Taj', 'Agra Fort Musamman Burj', 'Baby Taj morning'],
        'hotels': ['The Oberoi Amarvilas', 'ITC Mughal', 'Taj Hotel & Convention Centre', 'Crystal Sarovar Premiere'],
        'date_ideas': ['Taj Mahal at sunrise together', 'Mehtab Bagh sunset + shayari', 'Dinner at Oberoi Amarvilas with Taj view'],
        'hero_emoji': '🕌',
    },
    'varanasi': {
        'display_name': 'Varanasi',
        'tagline': 'The Oldest Love Story on Earth',
        'romantic_desc': 'Ghats, Ganga aarti, and 5000 years of devotion — Varanasi is love at its most ancient and spiritual.',
        'state': 'Uttar Pradesh',
        'places': ['Dashashwamedh Ghat', 'Manikarnika Ghat', 'Sarnath', 'Kashi Vishwanath Temple', 'Assi Ghat'],
        'cafes': ['Blue Lassi Shop', 'Brown Bread Bakery', 'Open Hand Cafe', 'Pizzeria Vaatika Cafe', 'Lotus Lounge'],
        'activities': ['Ganga Aarti at Dashashwamedh', 'Morning boat ride on Ganga', 'Silk shopping at Banaras'],
        'romantic_spots': ['Ganga sunrise boat ride', 'Assi Ghat morning chai', 'Dashashwamedh Ghat aarti evening', 'Ramnagar Fort sunset'],
        'hotels': ['Taj Ganges', 'BrijRama Palace', 'Suryauday Haveli', 'Ramada Plaza JHV'],
        'date_ideas': ['Sunrise boat ride on Ganga', 'Ganga Aarti together', 'Banarasi silk saree shopping'],
        'hero_emoji': '🪷',
    },
    'mysore': {
        'display_name': 'Mysore',
        'tagline': 'The Royal City of Fragrant Love',
        'romantic_desc': 'Palace lights, sandalwood breeze, and Chamundi Hills at sunset — Mysore is where love feels like royalty.',
        'state': 'Karnataka',
        'places': ['Mysore Palace', 'Chamundi Hills', 'Brindavan Gardens', 'St. Philomena\'s Church', 'Karanji Lake'],
        'cafes': ['Vinayaka Mylari (dosa!)', 'Depth N Green', 'Oyster Bay', 'La Mansion', 'Old House Cafe'],
        'activities': ['Mysore Palace illumination (Sunday)', 'Brindavan Gardens musical fountain', 'Chamundi Hill drive'],
        'romantic_spots': ['Mysore Palace lit up at night', 'Brindavan Gardens fountain show', 'Chamundi Hills sunset', 'Karanji Lake walk'],
        'hotels': ['Radisson Blu Plaza', 'Royal Orchid Metropole', 'Fortune JP Palace', 'Lalitha Mahal Palace Hotel'],
        'date_ideas': ['Palace illumination + dinner', 'Chamundi Hills sunrise drive', 'Brindavan Gardens fountain date'],
        'hero_emoji': '👑',
    },
    'pondicherry': {
        'display_name': 'Pondicherry',
        'tagline': 'French Kisses & Indian Beaches',
        'romantic_desc': 'Yellow streets, French quarters, and sunrise at Promenade — Pondicherry is India\'s most European love affair.',
        'state': 'Puducherry',
        'places': ['Promenade Beach', 'Auroville', 'French Quarter', 'Paradise Beach', 'Aurobindo Ashram'],
        'cafes': ['Cafe Des Arts', 'Le Dupleix', 'Baker Street', 'Coromandel Cafe', 'Zuka Chocolate'],
        'activities': ['Cycling through French Quarter', 'Sunrise at Rock Beach', 'Day trip to Auroville'],
        'romantic_spots': ['Promenade Beach sunrise', 'White Town colourful streets', 'Paradise Beach boat ride', 'Serenity Beach sunset'],
        'hotels': ['Palais De Mahe', 'La Villa', 'The Promenade', 'Hotel De L\'Orient'],
        'date_ideas': ['Cycle through White Town', 'Sunrise at Rock Beach + French breakfast', 'Paradise Beach boat trip'],
        'hero_emoji': '🇫🇷',
    },
    'darjeeling': {
        'display_name': 'Darjeeling',
        'tagline': 'Love Over a Cup of Tea',
        'romantic_desc': 'Kanchenjunga mornings, toy train memories, and warm chai that tastes like a hug — Darjeeling is love steeped in mist.',
        'state': 'West Bengal',
        'places': ['Tiger Hill', 'Batasia Loop', 'Mall Road', 'Peace Pagoda', 'Happy Valley Tea Estate'],
        'cafes': ['Glenary\'s Bakery', 'Keventers', 'Sonam\'s Kitchen', 'Gatty\'s Cafe', 'Kunga Restaurant'],
        'activities': ['Tiger Hill sunrise', 'Toy train (Darjeeling Himalayan Railway)', 'Tea estate walk'],
        'romantic_spots': ['Tiger Hill Kanchenjunga sunrise', 'Batasia Loop toy train view', 'Mall Road misty walk', 'Rock Garden waterfall'],
        'hotels': ['Mayfair Darjeeling', 'Windamere Hotel', 'Elgin Darjeeling', 'The Viceroy'],
        'date_ideas': ['Tiger Hill sunrise date', 'Toy train ride together', 'Tea tasting at Happy Valley'],
        'hero_emoji': '🍵',
    },
    'ooty': {
        'display_name': 'Ooty',
        'tagline': 'Queen of Hills, Queen of My Heart',
        'romantic_desc': 'Nilgiri tea gardens, misty lake mornings, and the smell of eucalyptus — Ooty is where love breathes fresh air.',
        'state': 'Tamil Nadu',
        'places': ['Ooty Lake', 'Botanical Garden', 'Doddabetta Peak', 'Rose Garden', 'Pykara Falls'],
        'cafes': ['King Star Confectionery', 'Willy\'s Coffee Pub', 'Sidewalk Cafe', 'Cafe Coffee Day Ooty', 'Ascot Restaurant'],
        'activities': ['Boating at Ooty Lake', 'Nilgiri Mountain Railway toy train', 'Tea factory visit'],
        'romantic_spots': ['Ooty Lake morning mist boat ride', 'Doddabetta Peak viewpoint', 'Rose Garden walk', 'Pykara Falls trek'],
        'hotels': ['Savoy Hotel (IHCL)', 'Sterling Ooty Elk Hill', 'Gem Park', 'King\'s Cliff'],
        'date_ideas': ['Ooty Lake boating + chocolate tasting', 'Toy train ride through tea gardens', 'Doddabetta Peak sunrise'],
        'hero_emoji': '🌿',
    },
    'alleppey': {
        'display_name': 'Alleppey (Alappuzha)',
        'tagline': 'Venice of the East — Floating in Love',
        'romantic_desc': 'Houseboat nights, backwater sunsets, and coconut-scented breeze — Alleppey is love floating on water.',
        'state': 'Kerala',
        'places': ['Alleppey Backwaters', 'Alappuzha Beach', 'Pathiramanal Island', 'Marari Beach', 'Kumarakom (nearby)'],
        'cafes': ['Halais Restaurant', 'Dreamers Cafe & Restaurant', 'Cassia Restaurant', 'Thaff Restaurant'],
        'activities': ['Houseboat cruise through backwaters', 'Canoe ride at sunrise', 'Beach walk at Marari'],
        'romantic_spots': ['Backwater sunset from houseboat', 'Pathiramanal Island morning', 'Marari Beach golden hour', 'Vembanad Lake sunrise'],
        'hotels': ['Marari Beach Resort (CGH)', 'Xandari Pearl', 'Lake Palace Resort', 'Punnamada Backwater Resort'],
        'date_ideas': ['Overnight houseboat stay', 'Sunrise canoe ride', 'Marari Beach dinner under stars'],
        'hero_emoji': '🛶',
    },
    'munnar': {
        'display_name': 'Munnar',
        'tagline': 'Love Grows Like Tea on These Hills',
        'romantic_desc': 'Endless tea carpets, misty drives, and the silence of green valleys — Munnar is where love whispers through the hills.',
        'state': 'Kerala',
        'places': ['Tea Gardens', 'Mattupetty Dam', 'Echo Point', 'Top Station', 'Eravikulam National Park'],
        'cafes': ['SN Restaurant', 'Rapsy Restaurant', 'Eastend Munnar', 'Tea County Restaurant'],
        'activities': ['Tea estate walk', 'Boating at Mattupetty Dam', 'Drive to Top Station'],
        'romantic_spots': ['Tea garden sunrise walk', 'Echo Point misty morning', 'Top Station endless valley view', 'Mattupetty Dam boat ride'],
        'hotels': ['Tea County', 'Windermere Estate', 'Spice Tree Munnar', 'Elysium Garden Hill Resorts'],
        'date_ideas': ['Tea garden walk at sunrise', 'Echo Point misty selfie', 'Top Station drive together'],
        'hero_emoji': '🍃',
    },
    'jodhpur': {
        'display_name': 'Jodhpur',
        'tagline': 'The Blue City of Bold Love',
        'romantic_desc': 'Blue-washed walls, Mehrangarh\'s majesty, and desert sunsets — Jodhpur is love painted in the boldest blue.',
        'state': 'Rajasthan',
        'places': ['Mehrangarh Fort', 'Jaswant Thada', 'Umaid Bhawan Palace', 'Clock Tower Market', 'Mandore Gardens'],
        'cafes': ['Stepwell Cafe', 'Nirvana Cafe', 'Jhankar Choti Haveli', 'Cafe Royale Mehrangarh'],
        'activities': ['Zipline at Mehrangarh Fort', 'Blue city walk at sunrise', 'Desert safari at Osian (nearby)'],
        'romantic_spots': ['Mehrangarh Fort sunset', 'Jaswant Thada marble reflections', 'Blue city rooftop sunrise', 'Umaid Bhawan Palace garden'],
        'hotels': ['Umaid Bhawan Palace (Taj)', 'Raas Jodhpur', 'Ajit Bhawan', 'Ratan Vilas'],
        'date_ideas': ['Sunrise over blue city from rooftop', 'Mehrangarh Fort sunset + zipline', 'Royal dinner at Umaid Bhawan'],
        'hero_emoji': '💙',
    },
    'amritsar': {
        'display_name': 'Amritsar',
        'tagline': 'Golden Love, Warm Hearts',
        'romantic_desc': 'The Golden Temple\'s divine glow, Wagah Border energy, and the warmth of Punjabi hospitality — Amritsar is love on a grand scale.',
        'state': 'Punjab',
        'places': ['Golden Temple', 'Jallianwala Bagh', 'Wagah Border', 'Partition Museum', 'Heritage Street'],
        'cafes': ['Brothers Dhaba', 'Kesar Da Dhaba', 'Bharawan Da Dhaba', 'Crystal Restaurant', 'All India Famous Amritsari Kulcha'],
        'activities': ['Golden Temple visit at dawn', 'Wagah Border ceremony', 'Food walk at Heritage Street'],
        'romantic_spots': ['Golden Temple at dawn (divine quiet)', 'Heritage Street evening lights', 'Wagah Border patriotic sunset', 'Ram Bagh garden walk'],
        'hotels': ['Hyatt Amritsar', 'Radisson Blu', 'ITC Welcomhotel', 'Hotel Hong Kong Inn'],
        'date_ideas': ['Golden Temple dawn visit + langar', 'Heritage Street food walk', 'Wagah Border together at sunset'],
        'hero_emoji': '🙏',
    },
    'srinagar': {
        'display_name': 'Srinagar',
        'tagline': 'Paradise on Earth, Love in Heaven',
        'romantic_desc': 'Dal Lake shikaras, Mughal gardens, and snow-kissed mountains — Srinagar is the most romantic postcard India has.',
        'state': 'Jammu & Kashmir',
        'places': ['Dal Lake', 'Shalimar Bagh', 'Nishat Bagh', 'Shankaracharya Temple', 'Pari Mahal'],
        'cafes': ['Ahdoo\'s', 'Chai Jaai', 'Cafe Liberty', 'Mughal Darbar', 'Books & Bricks Cafe'],
        'activities': ['Shikara ride on Dal Lake', 'Mughal Gardens walk', 'Stay on a houseboat'],
        'romantic_spots': ['Dal Lake shikara at sunset', 'Shalimar Bagh moonlit walk', 'Pari Mahal hilltop view', 'Nigeen Lake quiet morning'],
        'hotels': ['The Lalit Grand Palace', 'Vivanta Dal View', 'Houseboat on Dal Lake', 'Taj Vivanta'],
        'date_ideas': ['Sunset shikara ride on Dal Lake', 'Houseboat overnight stay', 'Mughal Garden walk + kahwa'],
        'hero_emoji': '🏔️',
    },
    'leh': {
        'display_name': 'Leh-Ladakh',
        'tagline': 'Love at the Top of the World',
        'romantic_desc': 'Pangong Lake, Khardung La, and skies so clear you can see forever — Leh is where love conquers every altitude.',
        'state': 'Ladakh',
        'places': ['Pangong Lake', 'Khardung La Pass', 'Leh Palace', 'Shanti Stupa', 'Magnetic Hill'],
        'cafes': ['The Tibetan Kitchen', 'Bon Appetit', 'Chopsticks Noodle Bar', 'Lala\'s Art Cafe', 'German Bakery'],
        'activities': ['Road trip to Pangong Lake', 'Camping at Pangong', 'Monastery hopping'],
        'romantic_spots': ['Pangong Lake blue water sunrise', 'Shanti Stupa golden hour', 'Khardung La top of world selfie', 'Nubra Valley sand dunes'],
        'hotels': ['The Grand Dragon', 'Chamba Camp Thiksey', 'Hotel & Camp Pangong', 'Stok Palace Heritage Hotel'],
        'date_ideas': ['Road trip to Pangong Lake', 'Camping under Ladakh stars', 'Shanti Stupa sunrise together'],
        'hero_emoji': '🗻',
    },
    'coorg': {
        'display_name': 'Coorg (Kodagu)',
        'tagline': 'The Scotland of India — Draped in Love',
        'romantic_desc': 'Coffee plantations, misty waterfalls, and the intoxicating scent of spice — Coorg is love wrapped in green velvet.',
        'state': 'Karnataka',
        'places': ['Abbey Falls', 'Raja\'s Seat', 'Talacauvery', 'Mandalpatti Peak', 'Namdroling Monastery'],
        'cafes': ['Coorg Cuisine (Raintree)', 'Taste of Coorg', 'Beerbell Cafe', 'Beans & Brews Cafe'],
        'activities': ['Coffee plantation walk', 'Mandalpatti Peak jeep drive', 'Abbey Falls trek'],
        'romantic_spots': ['Raja\'s Seat sunset', 'Abbey Falls misty morning', 'Mandalpatti Peak above clouds', 'Talacauvery sacred spring'],
        'hotels': ['Evolve Back (Orange County)', 'Tamara Coorg', 'Meriyanda Nature Lodge', 'Amanvana Spa Resort'],
        'date_ideas': ['Coffee plantation walk + tasting', 'Mandalpatti sunrise jeep ride', 'Spa day at Tamara Coorg'],
        'hero_emoji': '☕',
    },
    'andaman': {
        'display_name': 'Andaman Islands',
        'tagline': 'Turquoise Love in the Middle of Nowhere',
        'romantic_desc': 'Crystal clear waters, private beaches, and underwater worlds — Andaman is where love escapes to paradise.',
        'state': 'Andaman & Nicobar',
        'places': ['Radhanagar Beach', 'Cellular Jail', 'Elephant Beach', 'Neil Island', 'Baratang Island'],
        'cafes': ['Full Moon Cafe', 'Amaya Restaurant', 'New Lighthouse Restaurant', 'Anju Coco Restaurant'],
        'activities': ['Scuba diving at Havelock', 'Glass-bottom boat at Elephant Beach', 'Light & sound show at Cellular Jail'],
        'romantic_spots': ['Radhanagar Beach sunset (Asia\'s best)', 'Elephant Beach snorkeling', 'Neil Island natural bridge', 'Kalapathar Beach sunrise'],
        'hotels': ['Taj Exotica Resort', 'Barefoot at Havelock', 'Munjoh Ocean Resort', 'Silver Sand Beach Resort'],
        'date_ideas': ['Scuba diving together', 'Radhanagar Beach sunset + dinner', 'Neil Island day trip'],
        'hero_emoji': '🏝️',
    },
    'jaisalmer': {
        'display_name': 'Jaisalmer',
        'tagline': 'The Golden City of Desert Romance',
        'romantic_desc': 'Sand dunes at sunset, camel rides under stars, and a fort made of gold — Jaisalmer is love straight out of a desert fairy tale.',
        'state': 'Rajasthan',
        'places': ['Jaisalmer Fort', 'Sam Sand Dunes', 'Patwon Ki Haveli', 'Gadisar Lake', 'Kuldhara Ghost Village'],
        'cafes': ['Free Tibet Restaurant', '1st Gate Home Fusion', 'Kuku Coffee Shop', 'Cafe The Kaku'],
        'activities': ['Desert safari + camel ride', 'Cultural night at Sam Dunes', 'Fort walk at golden hour'],
        'romantic_spots': ['Sam Sand Dunes sunset', 'Gadisar Lake sunrise', 'Jaisalmer Fort golden hour', 'Stargazing in Thar Desert'],
        'hotels': ['Suryagarh', 'Hotel Rang Mahal', 'Mystic Jaisalmer', 'The Serai'],
        'date_ideas': ['Desert camping under stars', 'Sunset camel ride at Sam Dunes', 'Fort walk at golden hour'],
        'hero_emoji': '🐪',
    },
}


def get_odisha_cities():
    """Return only Odisha cities from the suggestions"""
    return {k: v for k, v in CITY_SUGGESTIONS.items() if v.get('state') == 'Odisha'}


def get_metro_cities():
    """Return only major metro cities"""
    return {k: v for k, v in CITY_SUGGESTIONS.items() if v.get('state') != 'Odisha'}


def get_plan_prompt(data):
    """Generate AI prompt based on user input"""
    
    relationship_type = data.get('relationship_type', 'girlfriend')
    vibe = data.get('vibe', 'romantic')
    city = data.get('city', '').lower()
    
    # Get city-specific suggestions
    city_info = ""
    if city in CITY_SUGGESTIONS:
        places = ", ".join(CITY_SUGGESTIONS[city]['places'][:3])
        cafes = ", ".join(CITY_SUGGESTIONS[city]['cafes'][:2])
        city_info = f"\n\nSUGGESTED PLACES IN {city.upper()}:\n- Must-visit spots: {places}\n- Recommended cafes: {cafes}"
    
    # Get personalization details
    personalization = ""
    if data.get('about_partner'):
        personalization += f"\n\nABOUT {data.get('partner_name', 'Partner').upper()}:\n{data.get('about_partner')}"
    if data.get('about_yourself'):
        personalization += f"\n\nABOUT YOUR RELATIONSHIP:\n{data.get('about_yourself')}"
    if data.get('special_request'):
        personalization += f"\n\nSPECIAL REQUESTS:\n{data.get('special_request')}"
    
    base_prompt = f"""You are a creative and fun Valentine's Day planner AI assistant.

USER DETAILS:
- Name: {data.get('your_name', 'User')}
{f"- Partner/Friend Name: {data.get('partner_name', 'Partner')}" if relationship_type != 'self_love' else '- This is a SELF-LOVE plan for themselves'}
- Relationship Type: {relationship_type}
- City/Location: {data.get('city', 'their city')}
- Budget: ₹{data.get('budget', '2000')}
- Planning Date: {data.get('plan_type', 'Valentine Day')}
- Vibe: {vibe}
{city_info}{personalization}

YOUR TASK:
Create a HIGHLY PERSONALIZED Valentine's plan that:
✨ Uses the personalization details to make it unique and special
💰 Stays within the budget
📱 Is social media friendly and shareable
🎁 Includes surprise elements based on their interests
💝 References specific details about them when suggesting activities

IMPORTANT: Use the personalization information to customize every suggestion!

"""

    # Different prompts for different relationship types
    if relationship_type == 'crush':
        base_prompt += """
SPECIAL INSTRUCTIONS FOR CRUSH MODE 😏:
- Keep it bold but not creepy
- Include "Send this at 11:11 PM and disappear 😈" type suggestions
- Add mysterious elements
- Suggest subtle but impactful gestures
- Include ice-breaker messages
- Make it exciting and slightly risky
"""
    elif relationship_type == 'best_friend':
        base_prompt += """
SPECIAL INSTRUCTIONS FOR BEST FRIEND / ANTI-VALENTINE MODE 🫂:
- Make it fun and roast-style
- Include pizza, movies, memes
- Add jokes about being single together
- Suggest late-night calls and comfort food
- Keep it light-hearted and wholesome
- No romantic pressure - pure friendship vibes
"""
    elif relationship_type == 'self_love':
        base_prompt += """
SPECIAL INSTRUCTIONS FOR SELF-LOVE MODE 😌:
- Focus on self-care, pampering, and personal growth
- Suggest solo activities: spa day, skincare routine, favorite food, journaling, shopping, reading, hobbies
- Include powerful affirmations and self-appreciation rituals
- No partner needed - this is ALL about celebrating YOU
- Make it empowering, confidence-boosting, and feel-good
- Suggest treating yourself to something special (favorite meal, new outfit, solo movie)
- Include a "letter to yourself" suggestion
- Add social media worthy self-love moments
"""
    else:
        base_prompt += """
SPECIAL INSTRUCTIONS FOR ROMANTIC MODE ❤️:
- Keep it sweet and thoughtful
- Include meaningful gestures
- Suggest heartfelt messages
- Add romantic surprises
- Balance between cute and passionate
"""

    # Get the plan type
    plan_type = data.get('plan_type', 'Valentine Day')
    
    # Duration-specific instructions
    if plan_type == 'Full Week':
        base_prompt += """

FORMAT YOUR OUTPUT AS FOLLOWS:

💖 VALENTINE'S WEEK PLAN 💖

**Day 1 - Rose Day (Feb 7) 🌹**
- **Activity**: [specific activity]
- **Gift Idea**: [affordable gift suggestion]
- **Cost**: ₹[amount]
- **Message to Send**: "[romantic/funny/bold message]"
- **Pro Tip**: [one insider tip]

**Day 2 - Propose Day (Feb 8) 💍**
[same format]

**Day 3 - Chocolate Day (Feb 9) 🍫**
[same format]

**Day 4 - Teddy Day (Feb 10) 🧸**
[same format]

**Day 5 - Promise Day (Feb 11) 🤝**
[same format]

**Day 6 - Hug Day (Feb 12) 🤗**
[same format]

**Day 7 - Kiss Day (Feb 13) 💋**
[same format]

**Day 8 - Valentine's Day (Feb 14) 💘**
- **Main Activity**: [special date plan]
- **Surprise Element**: [unexpected twist]
- **Gift Idea**: [meaningful gift]
- **Cost**: ₹[amount]
- **Final Message**: "[heartfelt message]"
- **Secret Move**: [one magical gesture]

💰 **Total Budget Used**: ₹[total]

✨ **BONUS SURPRISE IDEA**: [One unexpected romantic gesture]
"""
    else:
        # Individual day plans
        day_themes = {
            'Rose Day': ('Rose Day (Feb 7)', '🌹', 'roses, romantic gestures, red theme'),
            'Propose Day': ('Propose Day (Feb 8)', '💍', 'proposals, confessions, declarations'),
            'Chocolate Day': ('Chocolate Day (Feb 9)', '🍫', 'chocolates, sweets, indulgence'),
            'Teddy Day': ('Teddy Day (Feb 10)', '🧸', 'cuddly gifts, comfort, warmth'),
            'Promise Day': ('Promise Day (Feb 11)', '🤝', 'commitments, promises, future plans'),
            'Hug Day': ('Hug Day (Feb 12)', '🤗', 'warmth, closeness, physical affection'),
            'Kiss Day': ('Kiss Day (Feb 13)', '💋', 'intimacy, passion, romance'),
            'Valentine Day': ('Valentine\'s Day (Feb 14)', '💘', 'grand celebration, love, special moments'),
        }
        
        day_name, emoji, theme = day_themes.get(plan_type, ('Valentine\'s Day (Feb 14)', '💘', 'love and celebration'))
        
        base_prompt += f"""

FORMAT YOUR OUTPUT AS FOLLOWS:

{emoji} {day_name.upper()} PLAN {emoji}

**Theme**: Focus on {theme}

**Morning (9 AM - 12 PM) ☀️**
- **Activity**: [specific activity related to {day_name}]
- **Location**: [where to go]
- **Cost**: ₹[amount]
- **Message to Send**: "[message related to the day's theme]"

**Afternoon (12 PM - 5 PM) 🌤️**
- **Activity**: [specific activity]
- **Gift Idea**: [gift suggestion themed for {day_name}]
- **Location**: [where to go]
- **Cost**: ₹[amount]
- **Pro Tip**: [insider tip]

**Evening (5 PM - 9 PM) 🌙**
- **Main Date Activity**: [special activity fitting the theme]
- **Location**: [where to go]
- **Cost**: ₹[amount]
- **Message to Send**: "[romantic message]"

**Night (9 PM onwards) ✨**
- **Surprise Element**: [unexpected twist related to {day_name}]
- **Final Message**: "[heartfelt message perfect for {day_name}]"
- **Secret Move**: [magical gesture]

💰 **Total Budget Used**: ₹[total]

✨ **BONUS SURPRISE IDEA**: [One unexpected gesture themed for {day_name}]
"""

    base_prompt += """

IMPORTANT RULES:
✅ Keep suggestions realistic and affordable
✅ Use emojis generously to make it fun
✅ Include specific message examples
✅ Suggest local spots if city is known
✅ Add at least ONE surprise element
✅ Keep language clean and respectful
✅ Make it screenshot-worthy for social media
✅ Budget should not exceed the limit

Create an amazing plan now! 💘
"""

    return base_prompt


def generate_plan_with_ai(user_data):
    """Call OpenAI API to generate the Valentine plan"""
    
    if not settings.OPENAI_API_KEY:
        return generate_fallback_plan(user_data)
    
    try:
        prompt = get_plan_prompt(user_data)
        
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a creative Valentine's Day planner who creates fun, emotional, and viral-worthy plans."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=3000,
        )
        
        plan_content = response.choices[0].message.content
        
        # Format the content for better display
        plan_content = format_plan_content(plan_content)
        
        return plan_content
        
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return generate_fallback_plan(user_data)


def generate_fallback_plan(user_data):
    """Fallback plan when OpenAI API is not available"""
    
    your_name = user_data.get('your_name', 'You')
    partner_name = user_data.get('partner_name', 'Your Valentine')
    budget = user_data.get('budget', '2000')
    city = user_data.get('city', 'your city')
    
    # Get city-specific suggestions for fallback
    city_key = city.lower().strip()
    city_data = CITY_SUGGESTIONS.get(city_key, {})
    spot1 = city_data.get('romantic_spots', ['a romantic viewpoint'])[0] if city_data else 'a romantic viewpoint'
    cafe1 = city_data.get('cafes', ['a cozy cafe'])[0] if city_data else 'a cozy cafe'
    hotel1 = city_data.get('hotels', ['a nice hotel'])[0] if city_data else 'a nice hotel'
    
    plan = f"""<h2>💖 VALENTINE PLAN FOR {your_name.upper()} & {partner_name.upper()} 💖</h2>

<h3>Morning (9 AM - 12 PM) ☀️</h3>
<ul>
<li><strong>Activity</strong>: Start with a sweet breakfast at {cafe1}</li>
<li><strong>Location</strong>: {cafe1}, {city}</li>
<li><strong>Cost</strong>: ₹{int(int(budget) * 0.15)}</li>
<li><strong>Message to Send</strong>: "Good morning ❤️ Ready for the best day ever?"</li>
</ul>

<h3>Afternoon (12 PM - 5 PM) 🌤️</h3>
<ul>
<li><strong>Activity</strong>: Visit {spot1}</li>
<li><strong>Location</strong>: {city}</li>
<li><strong>Gift Idea</strong>: A handwritten letter + chocolates</li>
<li><strong>Cost</strong>: ₹{int(int(budget) * 0.25)}</li>
<li><strong>Pro Tip</strong>: Capture candid moments — they're the best memories!</li>
</ul>

<h3>Evening (5 PM - 9 PM) 🌙</h3>
<ul>
<li><strong>Main Date Activity</strong>: Romantic dinner at {hotel1}</li>
<li><strong>Location</strong>: {hotel1}, {city}</li>
<li><strong>Cost</strong>: ₹{int(int(budget) * 0.40)}</li>
<li><strong>Message to Send</strong>: "Being with you is my favorite place to be 💕"</li>
</ul>

<h3>Night (9 PM onwards) ✨</h3>
<ul>
<li><strong>Surprise Element</strong>: A playlist of songs that remind you of them</li>
<li><strong>Final Message</strong>: "Thank you for making every day feel like Valentine's Day ❤️"</li>
<li><strong>Secret Move</strong>: End the night with a heartfelt promise for the future</li>
</ul>

<p>💰 <strong>Total Budget Used</strong>: ₹{budget}</p>

<p>✨ <strong>BONUS SURPRISE IDEA</strong>: Create a photo album of your favorite memories together and present it at the end of the day!</p>
"""
    
    return plan


def generate_love_letter(user_data):
    """Generate a personalized love letter"""
    
    if not settings.OPENAI_API_KEY:
        return generate_fallback_letter(user_data)
    
    try:
        your_name = user_data.get('your_name', 'Someone special')
        partner_name = user_data.get('partner_name', 'Dear')
        relationship_type = user_data.get('relationship_type', 'girlfriend')
        
        prompt = f"""Write a heartfelt, emotional, Indian-style love letter from {your_name} to {partner_name}.

Relationship context: {relationship_type}

The letter should:
- Be deeply personal, emotional, innocent, and warm
- Have a soft Indian romance feel — like shayari in English
- Include specific reasons why they're special
- Be 8-12 lines of pure heartfelt emotion
- Sound like it was handwritten on rose-scented paper
- Do NOT be robotic, cheesy, or over-sexual
- Use simple, easy English — emotion over vocabulary
- Feel like a mix of Bollywood letter + handwritten diary
- End with a beautiful promise or declaration
- Addressed from "Your Forever" if no name, otherwise from {your_name}

Examples of tone:
- "The day I met you, even the rain felt like it was celebrating."
- "You are not just my love — you are my favorite hello and my hardest goodbye."
- "I don't need stars when your eyes are the brightest thing in my sky."

Make it screenshot-worthy, shareable, and deeply emotional. It should feel like a real love letter, not an AI-generated one.
"""
        
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a romantic Indian-style love letter writer. You write with deep emotion, innocence, and poetic warmth. Your words feel handwritten, personal, and deeply human. You never sound robotic or generic."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=800,
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return generate_fallback_letter(user_data)


def generate_fallback_letter(user_data):
    """Fallback love letter"""
    partner_name = user_data.get('partner_name', 'My Love')
    your_name = user_data.get('your_name', 'Me')
    
    return f"""Dear {partner_name},

Every moment with you feels like a beautiful dream I never want to wake up from. You've brought colors into my life I didn't even know existed.

Your smile is my favorite notification, your laugh is my favorite sound, and your presence is my favorite place to be. You make ordinary moments feel extraordinary.

The day I met you, even the wind whispered that something beautiful had begun. You are not just a part of my life — you are the reason my heart learned to sing.

I don't need grand gestures to love you. I just need you — your voice on a late-night call, your laughter in a crowded room, your hand finding mine in the dark.

Thank you for being you — perfectly imperfect, wonderfully real, and absolutely irreplaceable. You're not just my Valentine; you're my every day, my every prayer, my every heartbeat.

Forever and always yours,
{your_name} ❤️
"""


def generate_city_experience(city_slug):
    """Generate a rich Valentine experience landing page content for a city"""
    city_data = CITY_SUGGESTIONS.get(city_slug)
    if not city_data:
        return None

    display_name = city_data['display_name']
    tagline = city_data['tagline']
    romantic_desc = city_data['romantic_desc']
    spots = ', '.join(city_data.get('romantic_spots', []))
    hotels = ', '.join(city_data.get('hotels', []))
    date_ideas = ', '.join(city_data.get('date_ideas', []))
    cafes = ', '.join(city_data.get('cafes', []))
    places = ', '.join(city_data.get('places', []))

    # If no API key, return curated static content
    if not settings.OPENAI_API_KEY:
        return _get_fallback_city_experience(city_data, city_slug)

    try:
        prompt = f"""You are creating Valentine's Day experience content for a landing page about {display_name}, India.

City info:
- Tagline: "{tagline}"
- Romantic description: "{romantic_desc}"
- Top romantic spots: {spots}
- Best hotels: {hotels}
- Date ideas: {date_ideas}
- Cafes: {cafes}
- Places: {places}

Generate a JSON object with these EXACT keys. All values must be strings (or arrays of objects as specified):

{{
  "love_story_title": "A short romantic heading about love in {display_name} (8-12 words)",
  "love_story_text": "A 3-4 line poetic paragraph about why {display_name} is perfect for couples. Indian romantic tone, emotional, vivid. No bullet points.",
  "valentine_offer_title": "A catchy offer heading for Valentine's week experience in {display_name} (5-8 words)",
  "valentine_offer_text": "A 2-3 line romantic experience description — mention a specific hotel, candlelight dinner, sunrise, or surprise activity. End with a call to action.",
  "romance_spots": [
    {{"name": "spot name", "emoji": "relevant emoji", "desc": "One-line romantic description of the spot"}}
  ] (include 4-5 spots),
  "date_plan": [
    {{"time": "Morning/Afternoon/Evening/Night", "emoji": "emoji", "activity": "Short romantic activity description for that time"}}
  ] (include 4 time slots),
  "city_love_letter": "A 6-8 line heartfelt Indian-style love letter addressed to 'My Love' set in {display_name} — mention a city landmark, a sunset, and a promise. Soft, innocent, poetic. From 'Your Forever'."
}}

Return ONLY valid JSON. No markdown, no code blocks, no extra text.
"""

        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a romantic city experience curator. You create dreamy, emotional, Indian-flavored Valentine content. You output valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.85,
            max_tokens=2000,
        )

        import json
        raw = response.choices[0].message.content.strip()
        # Strip markdown code fence if present
        if raw.startswith('```'):
            raw = re.sub(r'^```(?:json)?\s*', '', raw)
            raw = re.sub(r'\s*```$', '', raw)
        ai_content = json.loads(raw)
        return ai_content

    except Exception as e:
        print(f"City experience AI error: {e}")
        return _get_fallback_city_experience(city_data, city_slug)


def _get_fallback_city_experience(city_data, city_slug):
    """Static fallback city experience content"""
    name = city_data['display_name']
    spots = city_data.get('romantic_spots', city_data.get('places', []))
    hotels = city_data.get('hotels', [])
    date_ideas = city_data.get('date_ideas', [])

    romance_spots = []
    emojis = ['💕', '🌅', '✨', '🌸', '🏰']
    for i, spot in enumerate(spots[:5]):
        romance_spots.append({
            'name': spot.split(' at ')[0] if ' at ' in spot else spot,
            'emoji': emojis[i % len(emojis)],
            'desc': spot,
        })

    date_plan = [
        {'time': 'Morning', 'emoji': '☀️', 'activity': date_ideas[0] if len(date_ideas) > 0 else f'Explore the beauty of {name}'},
        {'time': 'Afternoon', 'emoji': '🌤️', 'activity': date_ideas[1] if len(date_ideas) > 1 else f'Romantic cafe hopping in {name}'},
        {'time': 'Evening', 'emoji': '🌅', 'activity': date_ideas[2] if len(date_ideas) > 2 else f'Sunset at a romantic viewpoint'},
        {'time': 'Night', 'emoji': '🌙', 'activity': f'Candlelight dinner at {hotels[0]}' if hotels else f'Starlit dinner in {name}'},
    ]

    return {
        'love_story_title': f'Why {name} Is Made for Lovers',
        'love_story_text': city_data.get('romantic_desc', f'{name} is a city where every corner tells a love story.'),
        'valentine_offer_title': f'💝 Valentine\'s Week in {name}',
        'valentine_offer_text': f'Experience the most romantic week of your life in {name}. From sunrise surprises to candlelight dinners at {hotels[0] if hotels else "luxury hotels"}, we\'ve planned every heartbeat for you.',
        'romance_spots': romance_spots,
        'date_plan': date_plan,
        'city_love_letter': f'My Love,\n\nEvery sunset in {name} reminded me of you — warm, golden, and impossible to look away from. I found our names written in the wind at {spots[0] if spots else "every corner"}.\n\nYours forever,\nYour Forever ❤️',
    }
