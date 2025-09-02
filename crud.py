from models import Author, Paper, Topic, PaperTopic, PaperContent, session
from sqlalchemy import func

# Author CRUD operations
def add_author(name, affiliation=None, email=None):
    author = Author(
        name=name,
        affiliation=affiliation,
        email=email,
        total_papers=0
    )
    session.add(author)
    session.commit()
    return author

def view_all_authors():
    authors = session.query(Author).all()
    if authors:
        print("\n=== ALL AUTHORS ===")
        for author in authors:
            print(f"ID: {author.id} | Name: {author.name} | Affiliation: {author.affiliation or 'N/A'} | Papers: {author.total_papers}")
    else:
        print("No authors found.")

def get_author_papers(author_name):
    author = session.query(Author).filter(Author.name.ilike(f"%{author_name}%")).first()
    if author:
        papers = author.papers
        print(f"\n=== PAPERS BY {author.name.upper()} ===")
        for paper in papers:
            print(f"- {paper.title} ({paper.publication_year}) - {paper.journal or 'N/A'}")
    else:
        print(f"Author '{author_name}' not found.")

# Topic CRUD operations
def add_topic(name, description=None):
    topic = Topic(
        name=name,
        description=description
    )
    session.add(topic)
    session.commit()
    return topic

def view_all_topics():
    topics = session.query(Topic).all()
    if topics:
        print("\n=== ALL TOPICS ===")
        for topic in topics:
            paper_count = len(topic.papers)
            print(f"ID: {topic.id} | Name: {topic.name} | Papers: {paper_count}")
            if topic.description:
                print(f"  Description: {topic.description}")
    else:
        print("No topics found.")

# Paper CRUD operations
def add_paper(title, publication_year, journal, author_name, topic_names=None, content=None):
    # Find or create author
    author = session.query(Author).filter(Author.name.ilike(f"%{author_name}%")).first()
    if not author:
        author = add_author(author_name)
    
    paper = Paper(
        title=title,
        publication_year=publication_year,
        journal=journal,
        author=author
    )
    session.add(paper)
    session.flush()  # Get paper ID
    
    # Add content if provided
    if content:
        paper_content = PaperContent(paper_id=paper.id, content=content)
        session.add(paper_content)
    
    # Add topics if provided
    if topic_names:
        for topic_name in topic_names:
            topic = session.query(Topic).filter(Topic.name.ilike(f"%{topic_name}%")).first()
            if not topic:
                topic = add_topic(topic_name)
            
            paper_topic = PaperTopic(paper_id=paper.id, topic_id=topic.id)
            session.add(paper_topic)
    
    # Update author's total papers count
    author.total_papers = len(author.papers) + 1
    
    session.commit()
    return paper

def view_all_papers():
    papers = session.query(Paper).all()
    if papers:
        print("\n=== ALL PAPERS ===")
        for paper in papers:
            fav_status = "⭐" if paper.is_favorite else ""
            print(f"{fav_status} {paper.title} ({paper.publication_year})")
            print(f"  Author: {paper.author.name} | Journal: {paper.journal or 'N/A'}")
            
            # Show topics
            topics = [pt.topic.name for pt in paper.topics]
            if topics:
                print(f"  Topics: {', '.join(topics)}")
            print()
    else:
        print("No papers found.")

def toggle_favorite(paper_title):
    paper = session.query(Paper).filter(Paper.title.ilike(f"%{paper_title}%")).first()
    if paper:
        paper.is_favorite = 1 - paper.is_favorite  # Toggle between 0 and 1
        session.commit()
        status = "added to" if paper.is_favorite else "removed from"
        print(f"Paper '{paper.title}' {status} favorites.")
    else:
        print(f"Paper '{paper_title}' not found.")

def view_favorites():
    favorites = session.query(Paper).filter(Paper.is_favorite == 1).all()
    if favorites:
        print("\n=== FAVORITE PAPERS ===")
        for paper in favorites:
            print(f"⭐ {paper.title} ({paper.publication_year}) - {paper.author.name}")
    else:
        print("No favorite papers found.")

def search_papers_by_year(year):
    papers = session.query(Paper).filter(Paper.publication_year == year).all()
    if papers:
        print(f"\n=== PAPERS FROM {year} ===")
        for paper in papers:
            print(f"- {paper.title} by {paper.author.name}")
    else:
        print(f"No papers found from {year}.")

def search_papers_by_topic(topic_name):
    topic = session.query(Topic).filter(Topic.name.ilike(f"%{topic_name}%")).first()
    if topic:
        papers = [pt.paper for pt in topic.papers]
        print(f"\n=== PAPERS IN TOPIC: {topic.name.upper()} ===")
        for paper in papers:
            print(f"- {paper.title} ({paper.publication_year}) by {paper.author.name}")
    else:
        print(f"Topic '{topic_name}' not found.")

# Statistics functions
def get_stats():
    total_papers = session.query(Paper).count()
    total_authors = session.query(Author).count()
    total_topics = session.query(Topic).count()
    
    # Most common topics
    topic_counts = session.query(Topic.name, func.count(PaperTopic.id)).join(PaperTopic).group_by(Topic.name).order_by(func.count(PaperTopic.id).desc()).limit(3).all()
    
    # Most active authors
    active_authors = session.query(Author.name, Author.total_papers).order_by(Author.total_papers.desc()).limit(3).all()
    
    print("\n=== REPOSITORY STATISTICS ===")
    print(f"Total Papers: {total_papers}")
    print(f"Total Authors: {total_authors}")
    print(f"Total Topics: {total_topics}")
    
    if topic_counts:
        print("\nMost Common Topics:")
        for topic, count in topic_counts:
            print(f"  - {topic}: {count} papers")
    
    if active_authors:
        print("\nMost Active Authors:")
        for author, count in active_authors:
            print(f"  - {author}: {count} papers")