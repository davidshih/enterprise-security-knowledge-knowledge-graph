// 1. Internet-exposed critical workloads with open high-severity findings.
MATCH (f:Finding)-[:AFFECTS]->(w:Workload)
WHERE f.status = 'open'
  AND f.severity IN ['high', 'critical']
  AND w.internet_exposed = true
  AND w.criticality >= 4
RETURN w.name, f.title, f.severity
ORDER BY f.severity DESC;

// 2. Identities that can reach PCI data through at most six hops.
MATCH path = (i:Identity)-[*1..6]->(d:DataStore)
WHERE d.classification = 'pci'
RETURN i.display_name, d.name, relationships(path) AS access_path;

// 3. Public entry point to crown-jewel data attack paths.
MATCH path = (entry:CloudResource)-[*1..8]->(data:DataStore)
WHERE entry.internet_exposed = true
  AND data.criticality = 5
RETURN path
ORDER BY length(path) ASC
LIMIT 25;

// 4. Departed identities with residual access.
MATCH (i:Identity)-[r:MEMBER_OF|ASSUMES|CAN_ACCESS|CAN_ADMINISTER]->(target)
WHERE i.employment_status = 'terminated'
RETURN i.display_name, type(r), target.name, r.evidence_observed_at;

// 5. Findings whose exception expired but remain open.
MATCH (e:Exception)-[:EXCEPTS]->(f:Finding)
WHERE e.expires_at < datetime() AND f.status = 'open'
RETURN f.title, e.expires_at, e.approver_id;

// 6. Evidence freshness for privileged paths.
MATCH (i:Identity)-[r:CAN_ADMINISTER]->(w:Workload)
WHERE datetime(r.evidence_observed_at) < datetime() - duration('P1D')
RETURN i.display_name, w.name, r.evidence_observed_at;
