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

def handle_authors():
    while True:
        click.secho(".....AUTHORS.....", fg='yellow')
        click.secho('   1. Add New Author  \n   2. View All Authors  \n   3. View Author Papers  \n   4. Back to Main Menu', fg='blue')

        author_option = click.prompt("Select Author Option", type=int)

        if author_option == 1:
            click.secho('To add a new author...', fg='blue')
            name = click.prompt('Enter author name', type=str)
            affiliation = click.prompt('Enter affiliation (optional)', type=str, default='')
            email = click.prompt('Enter email (optional)', type=str, default='')
            
            if name:
                add_author(name, affiliation or None, email or None)
                click.secho('Author added successfully', fg='green')
                break
            else:
                click.secho('Author name is required', fg='red')

        elif author_option == 2:
            view_all_authors()
            click.pause()
            break

        elif author_option == 3:
            author_name = click.prompt('Enter author name to search', type=str)
            get_author_papers(author_name)
            click.pause()
            break

        elif author_option == 4:
            break

        else:
            click.secho("Invalid choice! Please select 1-4", fg='red')

    return research_repository()

def handle_papers():
    while True:
        click.secho(".....PAPERS.....", fg='yellow')
        click.secho('   1. Add New Paper  \n   2. View All Papers  \n   3. Back to Main Menu', fg='blue')

        paper_option = click.prompt("Select Paper Option", type=int)

        if paper_option == 1:
            click.secho('To add a new paper...', fg='blue')
            title = click.prompt('Enter paper title', type=str)
            year = click.prompt('Enter publication year', type=int)
            journal = click.prompt('Enter journal (optional)', type=str, default='')
            author_name = click.prompt('Enter author name', type=str)
            
            # Optional topics
            add_topics = click.confirm('Add topics to this paper?')
            topic_names = []
            if add_topics:
                while True:
                    topic = click.prompt('Enter topic name (or press Enter to finish)', type=str, default='')
                    if not topic:
                        break
                    topic_names.append(topic)
            
            # Optional content
            add_content = click.confirm('Add content/abstract to this paper?')
            content = None
            if add_content:
                content = click.prompt('Enter paper content/abstract', type=str)
            
            if title and author_name:
                add_paper(title, year, journal or None, author_name, 
                         topic_names if topic_names else None, content)
                click.secho('Paper added successfully', fg='green')
                break
            else:
                click.secho('Title and author name are required', fg='red')

        elif paper_option == 2:
            view_all_papers()
            click.pause()
            break

        elif paper_option == 3:
            break

        else:
            click.secho("Invalid choice! Please select 1-3", fg='red')

    return research_repository()

def handle_topics():
    while True:
        click.secho(".....TOPICS.....", fg='yellow')
        click.secho('   1. Add New Topic  \n   2. View All Topics  \n   3. Back to Main Menu', fg='blue')

        topic_option = click.prompt("Select Topic Option", type=int)

        if topic_option == 1:
            click.secho('To add a new topic...', fg='blue')
            name = click.prompt('Enter topic name', type=str)
            description = click.prompt('Enter description (optional)', type=str, default='')
            
            if name:
                add_topic(name, description or None)
                click.secho('Topic added successfully', fg='green')
                break
            else:
                click.secho('Topic name is required', fg='red')

        elif topic_option == 2:
            view_all_topics()
            click.pause()
            break

        elif topic_option == 3:
            break

        else:
            click.secho("Invalid choice! Please select 1-3", fg='red')

    return research_repository()

def handle_search_favorites():
    while True:
        click.secho(".....SEARCH & FAVORITES.....", fg='yellow')
        click.secho('   1. Search Papers by Year  \n   2. Search Papers by Topic  \n   3. Toggle Paper Favorite  \n   4. View Favorite Papers  \n   5. Back to Main Menu', fg='blue')

        search_option = click.prompt("Select Search Option", type=int)

        if search_option == 1:
            year = click.prompt('Enter publication year', type=int)
            search_papers_by_year(year)
            click.pause()
            break

        elif search_option == 2:
            topic_name = click.prompt('Enter topic name', type=str)
            search_papers_by_topic(topic_name)
            click.pause()
            break

        elif search_option == 3:
            paper_title = click.prompt('Enter paper title to toggle favorite', type=str)
            toggle_favorite(paper_title)
            click.pause()
            break

        elif search_option == 4:
            view_favorites()
            click.pause()
            break

        elif search_option == 5:
            break

        else:
            click.secho("Invalid choice! Please select 1-5", fg='red')

    return research_repository()

if __name__ == "__main__":
    research_repository()