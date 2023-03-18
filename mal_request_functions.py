from jikanpy import Jikan
from typing import Optional,Dict,Any
import datetime
jikan = Jikan()

def anime(id: int) -> Dict[str,Any]:
    all_dict = jikan.anime(id)
    #returning only relevant data
    title = all_dict['data']['title']
    title_eng = all_dict['data']['title_english']
    title_jap = all_dict['data']['title_japanese']
    episodes = all_dict['data']['episodes']
    status = all_dict['data']['status']
    duration = all_dict['data']['duration']
    rating = all_dict['data']['rating']
    score = all_dict['data']['score']
    rank = all_dict['data']['rank']
    popularity = all_dict['data']['popularity']
    synopsis = all_dict['data']['synopsis']
    year = all_dict['data']['year']

    genres = []
    for i in range(len(all_dict["data"]["genres"])):
        genres.append(all_dict['data']['genres'][i]['name'])
    
    return {"Title":title,
            "Title English":title_eng,
            "Title Japanese":title_jap,
            "Status":status,
            "Year":year,
            "Genres":genres,
            "Rating":rating,
            "Score":score,
            "Rank":rank,
            "Episodes":episodes,
            "Duration":duration,
            "Popularity":popularity,
            "Synopsis":synopsis}

def manga(id: int) -> Dict[str,Any]:
    all_dict = jikan.manga(id)
    #returning only relevant data
    title = all_dict['data']['title']
    title_eng = all_dict['data']['title_english']
    title_jap = all_dict['data']['title_japanese']
    chapters = all_dict['data']['chapters']
    volumes = all_dict['data']['volumes']
    status = all_dict['data']['status']
    score = all_dict['data']['score']
    rank = all_dict['data']['rank']
    popularity = all_dict['data']['popularity']
    synopsis = all_dict['data']['synopsis']

    authors = []
    for i in range(len(all_dict["data"]["authors"])):
        authors.append(all_dict['data']['authors'][i]['name'])

    genres = []
    for i in range(len(all_dict["data"]["genres"])):
        genres.append(all_dict['data']['genres'][i]['name'])
    for j in range(len(all_dict["data"]["explicit_genres"])):
        genres.append(all_dict['data']['explicit_genres'][i]['name'])
    
    return {"Title":title,
            "Title English":title_eng,
            "Title Japanese":title_jap, 
            "Author(s)":authors,
            "Status":status,
            "Genres":genres,
            "Score":score,
            "Rank":rank,
            "Volumes":volumes,
            "Chapters":chapters,
            "Popularity":popularity,
            "Synopsis":synopsis}
            
def character(id: int) -> Dict[str,Any]:
    all_dict = jikan.characters(id)['data']
    name = all_dict['name']
    kanji_name = all_dict['name_kanji']
    about = all_dict['about']

    return {"Name":name,
            "Name in Kanji": kanji_name,
            "About":about}

def current_season():
    date = datetime.date.today()
    md = date.month * 100 + date.day

    if ((md > 320) and (md < 621)):
        s = "spring"
    elif ((md > 620) and (md < 923)):
        s = "summer"
    elif ((md > 922) and (md < 1223)):
        s = "fall"
    else:
        s = "winter"

    return s

def current_year():
    return datetime.date.today().year

def season(year: Optional[int] = None,season: Optional[str] = None) -> Dict[str,Any]:
    if season:
        all_dict = jikan.seasons(year,season,parameters={'filter':'score'})['data']
    else:
        all_dict = jikan.seasons(year,parameters={'filter':'score'})['data']
    anime_dict = {}
    for i in range(len(all_dict)):
        anime_dict[all_dict[i]['title']] = [all_dict[i]['title_english'],all_dict[i]['mal_id']]
    return anime_dict

def schedule(day: Optional[str] = datetime.datetime.today().strftime("%A")) -> Dict[str,Any]:
    all_dict = jikan.schedules(day = day)["data"]
    schedule_dict = {}
    for i in range(len(all_dict)):
        schedule_dict[all_dict[i]['title']] = [all_dict[i]['title_english'],all_dict[i]['mal_id']]
    return schedule_dict

def search(typ: str, query: str) -> Dict[str,str]:
    all_dict = jikan.search(typ,query)['data']
    malid_dict = {}     #dict of MAL IDs of matching anime/manga with malid as key and title as value
    for i in range(len(all_dict)):
        malid_dict[all_dict[i]['mal_id']] = all_dict[i]['title']
    return malid_dict
