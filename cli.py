from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import mal_request_functions as request
from jikanpy import exceptions

def compare(option,cat,change_option = 0): #change options is to change the category to the respective number
    if not change_option: 
        for i in cat:
            if option.lower() == i.lower(): #to check if given user input matches a value in possible actions (categories list)
                return True
                break
        else:
            return False
    else:
        for i in cat:
            if option.lower() == i.lower():
                return cat.index(i) #to return the index of the category if they have inputted the name

def main(): #TODO: main menu function with looping
    console = Console()

    table_options = Table(show_lines = "True",style="#ccff00")
    table_options.add_column("[u]Sl No.[/u]",justify="center")
    table_options.add_column("[u]Options[/u]",justify = "center")

    categories = ["Anime by MAL ID","Manga by MAL ID","Character by MAL ID","Season","Schedule","Search"] #possible actions
    for row_no in range(1,len(categories)+1):
        table_options.add_row(str(row_no),categories[row_no-1])
    console.print("Select one of the options from below table")
    console.print(table_options)
    option = Prompt.ask("Enter chosen option:",default = "Schedule") #if none of the options are selected then schedule is taken by default
    
    if compare(option,categories) or (option.isdigit() and 0<int(option)<len(categories)+1): #if input is valid option or sl no
        if compare(option,categories):
            option = compare(option,categories,1) + 1 #to get sl no if name of option is given

        match int(option):
            case 1: #anime by mal id
                try:
                    id = Prompt.ask("Enter mal id of anime") 
                    data = request.anime(int(id))
                except exceptions.APIException:
                    console.print("Anime with that ID could not be found",style="red")
                except ValueError:
                    console.print("Enter valid ID",style= "red")
                else:
                    data_table = Table(show_lines=True,title = data["Title"],show_header=False)
                    for value in list(data.keys())[1:]:
                        data_table.add_row(str(value),str(data[value])) #field name,field value
                    console.print(data_table)

            case 2: #manga by mal id
                try:
                    id = Prompt.ask("Enter mal id of manga")
                    data = request.manga(int(id))
                except exceptions.APIException:
                    console.print("Manga with that ID could not be found",style="red")
                except ValueError:
                    console.print("Enter valid ID",style= "red")
                else:
                    data_table = Table(show_lines=True,title = data["Title"],show_header=False)
                    for value in list(data.keys())[1:]:
                        data_table.add_row(str(value),str(data[value])) #field name, field value
                    console.print(data_table)

            case 3: #character by mal id
                try:
                    id = Prompt.ask("Enter mal id of character")
                    data = request.character(int(id))
                except exceptions.APIException:
                    console.print("Character with that ID could not be found",style="red")
                except ValueError:
                    console.print("Enter valid ID",style= "red")
                else:
                    data_table = Table(show_lines=True,title = data["Name"],show_header = False)
                    for value in list(data.keys()):
                        data_table.add_row(str(value),str(data[value]))
                    console.print(data_table)

            case 4: #season
                try:
                    year = Prompt.ask("Enter year",default=str(request.current_year()))
                    season = Prompt.ask("Enter season",default=request.current_season())
                    data = request.season(year,season)
                except exceptions.APIException:
                    console.print("Enter valid ID",style="red")
                except ValueError:
                    console.print("Enter valid ID",style= "red")
                else:
                    data_table = Table(show_lines=True,title = f"Anime in {year} {season} ordered by score")
                    data_table.add_column("[u]Name[/u]",justify = "center")
                    data_table.add_column("[u]English Name[/u]",justify = "center")
                    data_table.add_column("[u]MAL_ID[/u]",justify = "center")

                    for i in data:
                        data_table.add_row(str(i),str(data[i][0]),str(data[i][1]))
                    console.print(data_table)

            case 5: #schedule
                day = Prompt.ask("Enter day",default=None)
                data_table = Table(show_lines=True,title = "Schedule")
                data_table.add_column("[u]Name[/u]",justify = "center")
                data_table.add_column("[u]English Name[/u]",justify = "center")
                data_table.add_column("[u]MAL_ID[/u]",justify = "center")
                
                while True: #so that day has a valid value
                    if day:     #if day is None or string
                        if day.lower() in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']:
                            data = request.schedule(day)
                            break
                        else:
                            console.print("Enter valid day",style = "red")
                            day = Prompt.ask("Enter day",default=None)
                            continue
                    else:
                        data = request.schedule()
                        break
                for i in data:
                    data_table.add_row(str(i),str(data[i][0]),str(data[i][1]))
                console.print(data_table)

            case 6: #search
                try:
                    typ = Prompt.ask("Enter anime or manga",default = "anime")
                    if typ == 'anime' or typ == 'manga':
                        que = Prompt.ask(f"Enter {typ} name")
                    else:
                        raise ValueError
                    data = request.search(typ,que)
                except exceptions.APIException:
                    console.print(f"{typ} with that ID could not be found",style="red")
                except ValueError:
                    console.print("Enter valid data",style= "red")
                else:
                    matching_table = Table(show_lines=True,title = f"Matching {typ}")
                    matching_table.add_column("[u]MAL ID[/u]",justify = "center")
                    matching_table.add_column("[u]English Name[/u]",justify = "center")
                    for i in data:
                        matching_table.add_row(str(i),data[i])
                    console.print(matching_table) #table with matching anime 

                    try:
                        if typ=='anime':
                            id = Prompt.ask("Enter MAL ID of selected anime")
                            data = request.anime(int(id))
                        else:
                            id = Prompt.ask("Enter MAL ID of selected manga")
                            data = request.manga(int(id))
                    except exceptions.APIException:
                        console.print("Anime with that ID could not be found",style="red")
                    except ValueError:
                        console.print("Enter valid ID",style= "red")
                    else:
                        data_table = Table(show_lines=True,title = data["Title"],show_header=False)
                        for value in list(data.keys())[1:]:
                            data_table.add_row(str(value),str(data[value]))
                        console.print(data_table)


    else:
        console.print("Enter valid option",style="red")

if __name__ == "__main__":
    main()