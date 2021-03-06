MATCH (person:Person), (company:Company)
WHERE person.company_id = company.id
CREATE (person)-[:WORKS_AT]->(company);

MATCH (coworker:Coworker), (office:Office)
WHERE coworker.office_id = office.id
CREATE (coworker)-[:WORKS_AT]->(office);

MATCH (deal:Deal), (person:Person)
WHERE deal.person_id = person.id
CREATE (deal)<-[:RESPONSIBLE_FOR]-(person);

MATCH (deal:Deal), (coworker:Coworker)
WHERE deal.coworker_id = coworker.id
CREATE (deal)<-[:SALESPERSON_FOR]-(coworker);

MATCH (document:Document), (person:Person)
WHERE document.person_id = person.id
CREATE (document)<-[:OWNS]-(person);

MATCH (document:Document), (deal:Deal)
WHERE document.deal_id = deal.id
CREATE (document)-[:ATTACHED_TO]->(deal);

MATCH (history:History), (person:Person)
WHERE history.person_id = person.id
CREATE (history)<-[:ATTENDED]-(person);

MATCH (history:History), (coworker:Coworker)
WHERE history.coworker_id = coworker.id
CREATE (history)<-[:ATTENDED]-(coworker);

MATCH (history:History), (document:Document)
WHERE history.document_id = document.id
CREATE (history)<-[:ATTACHED_TO]-(document);

MATCH (history:History), (deal:Deal)
WHERE history.deal_id = deal.id
CREATE (history)-[:PART_OF]->(deal);

// MATCH (r:Relationship), (p1:Person), (p2:Person)
// WHERE r.from_person_id = p1.id AND r.to_person_id = p2.id
// CREATE (p1)-[:RELATED_TO {type: r.type}]->(p2);