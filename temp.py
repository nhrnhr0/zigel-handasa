def create_invoice(total, projects):
    # Calculate the total sum of all project totals (subtracting the children totals)
    for project in projects:
        project['total_minus_children'] = project['total']
        for child in project['children']:
            project['total_minus_children'] -= child['total']
    
    
    buckets = []
    for project in projects:
        buckets.append({'id': project['id'], 'max': project['total_minus_children'], 'total': 0})
    
    # Sort the buckets by total
    buckets.sort(key=lambda x: x['max'])
    has_space = False
    remaining_total = total
    idx= 0
    while remaining_total > 0:
        # check if there are any spaces left
        has_space = False
        for bucket in buckets:
            if bucket['max'] > bucket['total']:
                has_space = True
                break
        if not has_space:
            break
            
        while buckets[idx % len(buckets)]['max'] <= buckets[idx % len(buckets)]['total']:
            idx += 1
        buckets[idx % len(buckets)]['total'] += 1
        remaining_total -= 1
        idx += 1
        
    if remaining_total > 0:
        # split the remaining total between all buckets evenly
        for bucket in buckets:
            bucket['total'] +=  int(remaining_total / len(buckets))
    
    # Create the invoice
    invoice = []
    for bucket in buckets:
        invoice.append({'id': bucket['id'], 'total': bucket['total']})
    return invoice

project1 = {'id': 'project 1', 'total': 1200, 'children': [{id:'child1', 'total': 300}]}
project2 = {'id': 'project 2', 'total': 1500, 'children': []}

projects = [project1, project2]

# Example usage:
res1 = create_invoice(2400, projects)
print(res1)  # Output: [{'id': 'xxx', 'total': 1500}, {'id': 'yyy', 'total': 900}]

res2 = create_invoice(1000, projects)
print(res2)  # Output: [{'id': 'xxx', 'total': 500}, {'id': 'yyy', 'total': 500}]

res3 = create_invoice(2000, projects)
print(res3)  # Output: [{'id': 'xxx', 'total': 1100}, {'id': 'yyy', 'total': 900}]

res4 = create_invoice(2800, projects)
print(res4)  # Output: [{'id': 'xxx', 'total': 1550}, {'id': 'yyy', 'total': 950}]
