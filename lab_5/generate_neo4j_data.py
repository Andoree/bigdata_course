import os
import random
from argparse import ArgumentParser

DOMAINS = ["biology", "physics", "mathematics"]


class Article:

    def __init__(self, article_id, domain, name):
        self.domain = domain
        self.name = name


class Reference:

    def __init__(self, source_article, target_article):
        self.source = source_article
        self.target = target_article


def main():
    parser = ArgumentParser()
    parser.add_argument('--output_path', default="neo4j_scripts.txt")
    parser.add_argument('--num_nodes', type=int, default=100)
    parser.add_argument('--num_edges', type=int, default=50)
    args = parser.parse_args()

    num_nodes = args.num_nodes
    num_edges = args.num_edges
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and output_dir != '':
        os.makedirs(output_dir)
    articles_list = []
    for i in range(num_nodes):
        domain = random.choice(DOMAINS)
        article_name = f"{domain}_article_{i}"
        article = Article(domain=domain, name=article_name, article_id=i)
        articles_list.append(article)
    references_list = []
    for i in range(num_edges):
        selected_articles = random.sample(articles_list, 2)
        source_article = selected_articles[0]
        target_article = selected_articles[1]
        reference = Reference(source_article=source_article, target_article=target_article)
        references_list.append(reference)
    with open(output_path, 'w+', ) as output_file:
        for article in articles_list:
            output_file.write(
                f"CREATE (a: Article {{domain: '{article.domain}', name: '{article.name}'}});\n")
        for reference in references_list:
            source_article = reference.source
            target_article = reference.target
            output_file.write("MATCH (a:Article),(b:Article)\n")
            output_file.write(f"WHERE a.name = '{source_article.name}' AND b.name = '{target_article.name}'\n")
            output_file.write("CREATE (a)-[r:Reference]->(b)\n")
            output_file.write("RETURN r;\n")


if __name__ == '__main__':
    main()
