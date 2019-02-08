from neo4j import GraphDatabase
from statistics import median
from random import randint
import json


def load_data(filepath="out/output.json"):
    f = open(filepath, 'r')
    data = json.loads(f.read())
    f.close()
    return data


def random_entry(data, table_name, column):
    table = data[table_name]
    random_row = table[randint(0, len(table))]
    return random_row[column]


def run_query(transaction, query, inputs=[]):
    def execute(tx):
        result = tx.run(query.format(*inputs)).consume()
        return result.t_first

    return transaction(execute)


def get_stats(exec, amount=100):
    print(median([exec() for i in range(amount)]))


if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

    data = load_data()

    with driver.session() as session:
        get_stats(lambda: run_query(session.read_transaction, '''
             MATCH (c: Company)
             RETURN c.name, c.id;
         '''))

        get_stats(lambda: run_query(session.read_transaction, '''
            MATCH (p:Person)-[:RESPONSIBLE_FOR]->(d: Deal)
            MATCH (p)-[WORKS_AT]->(c: Company)
            WHERE d.probability > {}
            RETURN p.name, p.position, p.email, p.phone, d.name, c.name;
        ''', [random_entry(data, 'deals', 'probability')]))

        get_stats(lambda: run_query(session.read_transaction, '''
            MATCH (deal:Deal)-[:PART_OF]->(history:History)<-[:ATTACHED_TO]-(document:Document)
            MATCH (coworker:Coworker)-[:ATTENDED]->(history)<-[:ATTENDED]-(person:Person)
            WHERE history.id = {}
            RETURN history.id, history.type, history.date, coworker.name, person.name, document.description;
        ''', [random_entry(data, 'histories', 'id')]))

        get_stats(lambda: run_query(session.read_transaction, '''
            MATCH (p: Person)-[:WORKS_AT]->(c:Company)
            WHERE c.id = {}
            RETURN p.name, c.name;
        ''', [random_entry(data, 'companies', 'id')]))