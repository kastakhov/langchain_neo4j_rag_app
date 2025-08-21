examples_prompt = """\
User input: {question}
Cypher query: {query}
"""

examples = [
    {
        "question": "Match all nodes and return all nodes.",
        "query": """\
MATCH (n) 
RETURN n AS node
"""
    },
    {
        "question": "Match all Patient nodes with an HAS relationship connected to a Visit node, and return the name of the visitors.",
        "query": """\
MATCH (n:Patient)-[:HAS]->(:Visit) 
RETURN n.name AS visitors
"""
    },
    {
        "question": "Bind a path pattern to a path variable, and return the path pattern.",
        "query": """\
MATCH p=(:Patient)-[:HAS]->(:Visit)
RETURN p AS path
"""
    },
    {
        "question": "Find and return all pairs of directly connected nodes that share the same label, where the first node in the pair does not have the property attribute with `IGNORE_ME` value.",
        "query": """\
MATCH (n:Label)-->(m:Label)
WHERE n.property <> 'IGNORE_ME'
RETURN n, m
"""
    },
    {
        "question": "Find the names of all nodes that are either labeled 'A' or 'B'.",
        "query": """\
MATCH (n) 
WHERE n:A|B 
RETURN n.name AS name
"""
    },
    {
        "question": "Find the names of relationships of type 'R1' or 'R2' between nodes with a specific label.",
        "query": """\
MATCH (n:Label)-[r]->(m:Label)
WHERE r:R1|R2
RETURN r.name AS name
"""
    },
    {
        "question": "Find the names of patients older than 30 who are known by a patient named Andy.",
        "query": """\
WITH 30 AS minAge 
MATCH (a:Patient WHERE a.name = 'Andy')-[:KNOWS]->(b:Patient WHERE b.age > minAge)
RETURN b.name
"""
    },
    {
        "question": "Find the names of patients who are friends of a patient named Andy.",
        "query": """\
MATCH (a:Patient {{name: 'Andy'}})
RETURN [(a)-->(b WHERE b:Patient) | b.name] AS friends
"""
    },
    {
        "question": "Find the 'since' years of 'KNOWS' relationships that were established before the year 2000 between patients.",
        "query": """\
WITH 2000 AS minYear
MATCH (a:Patient)-[r:KNOWS WHERE r.since < minYear]->(b:Patient)
RETURN r.since
"""
    },
    {
        "question": "Find the years when a patient named Andy knew other patients before the year 2000",
        "query": """\
WITH 2000 AS minYear
MATCH (a:Patient {{name: 'Andy'}})
RETURN [(a)-[r:KNOWS WHERE r.since < minYear]->(b:Patient) | r.since] AS years
"""
    },
    {
        "question": "Return the value of all variables.",
        "query": """\
MATCH (n:Label)-[r]->(m:Label)
RETURN *
"""
    },
    {
        "question": "Use alias for result column name.",
        "query": """\
MATCH (n:Label)-[r]->(m:Label)
RETURN n AS node, r AS rel
"""
    },
    {
        "question": "Return unique rows.",
        "query": """\
MATCH (n:Patient)-[r:KNOWS]-(m:Patient) 
RETURN DISTINCT n AS node
"""
    },
    {
        "question": "Match all nodes and sort results by name in ascending order.",
        "query": """\
MATCH (n)
RETURN n 
    ORDER BY n.name ASC
"""
    },
    {
        "question": "Match all nodes and sort results by name in descending order.",
        "query": """\
MATCH (n)
RETURN n
    ORDER BY n.name DESC
"""
    },
    {
        "question": "Match all nodes and skip first 5 results.",
        "query": """\
MATCH (n)
RETURN n
    SKIP 10
"""
    },
    {
        "question": "Match all nodes and limit results to 5.",
        "query": """\
MATCH (n)
RETURN n
    LIMIT 5
"""
    },
    {
        "question": "Match all nodes and count the number of nodes.",
        "query": """\
MATCH (n)
RETURN count(n) AS count
"""
    },
    {
        "question": "Match all patient who has more than 10 friends.",
        "query": """\
MATCH (p:PATIENT)-[:KNOWS]->(friend) 
WITH p, COUNT(friend) AS friendsCount
WHERE friendsCount > 10
RETURN p
"""
    },
    {
        "question": "Who is the oldest patient and how old are they?",
        "query": """\
MATCH (p:Patient)
RETURN p.name AS oldest_patient, duration.between(date(p.dob), date()).years AS age 
    ORDER BY age DESC
    LIMIT 1
"""
    },
    {
        "question": "Which physician has billed the least to Cigna.",
        "query": """\
MATCH (p:Payer)<-[c:COVERED_BY]-(v:Visit)-[t:TREATS]-(phy:Physician) 
WHERE p.name = 'Cigna' 
RETURN phy.name AS physician_name, SUM(c.billing_amount) AS total_billed 
    ORDER BY total_billed
    LIMIT 1
"""
    },
    {
        "question": "Which state had the largest percent increase in Cigna visits from 2022 to 2023?",
        "query": """\
MATCH (h:Hospital)<-[:AT]-(v:Visit)-[:COVERED_BY]->(p:Payer)
WHERE p.name = 'Cigna' AND v.admission_date >= '2022-01-01' AND
v.admission_date < '2023-12-31'
WITH h.state_name AS state, COUNT(v) AS visit_count,
    SUM(CASE WHEN v.admission_date >= '2022-01-01' AND
    v.admission_date < '2023-01-01' THEN 1 ELSE 0 END) AS count_2022,
    SUM(CASE WHEN v.admission_date >= '2023-01-01' AND
    v.admission_date < '2023-12-31' THEN 1 ELSE 0 END) AS count_2023
WITH state, visit_count, count_2022, count_2023,
    (toFloat(count_2023) - toFloat(count_2022)) / toFloat(count_2022) * 100
    AS percent_increase
RETURN state, percent_increase
ORDER BY percent_increase DESC
LIMIT 1
"""
    },
    {
        "question": "How many non-emergency patients in North Carolina have written reviews?",
        "query": """\
MATCH (r:Review)<-[:WRITES]-(v:Visit)-[:AT]->(h:Hospital)
WHERE h.state_name = 'NC' and v.admission_type <> 'Emergency'
RETURN count(*)
"""
    },
    {
        "question": "Find all patients billed in 2023 and their bill amount.",
        "query": """\
MATCH (v:Visit)-[c:COVERED_BY]->(p:Payer)
WHERE v.admission_date >= '2023-01-01' AND v.admission_date < '2023-12-31' AND p.name IS NOT NULL
RETURN p.name AS Payer, SUM(c.billing_amount) AS total_billing_amount
"""
    }
]