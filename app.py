import click 
from datetime import datetime
from models import Author, Paper, Topic, PaperTopic, PaperContent, session
from crud import (add_author, add_paper, add_topic, view_all_authors, view_all_papers, 
                 view_all_topics, get_author_papers, toggle_favorite, view_favorites,
                 search_papers_by_year, search_papers_by_topic, get_stats)

def research_repository():
    click.secho("Welcome To Research Paper Repository Manager", fg='blue', bg="white", bold=True)
    click.secho('Select an option to proceed', fg="yellow")
    click.secho('   1. Authors  \n   2. Papers  \n   3. Topics  \n   4. Search & Favorites  \n   5. Statistics  \n   6. Exit Program', fg='blue')

    choice = click.prompt("Select Option", type=int)

    if choice not in [1, 2, 3, 4, 5, 6]:
        click.secho("Invalid choice! Please select 1-6 to proceed", fg='red')
        return research_repository()

    if choice == 1:
        handle_authors()
    elif choice == 2:
        handle_papers()
    elif choice == 3:
        handle_topics()
    elif choice == 4:
        handle_search_favorites()
    elif choice == 5:
        get_stats()
        click.pause()
        return research_repository()
    elif choice == 6:
        click.secho("Exiting program. Goodbye!", fg='green')
        return
