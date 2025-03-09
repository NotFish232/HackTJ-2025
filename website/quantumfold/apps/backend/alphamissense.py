

def get_alphamissense_result(uniprot_id, mutation_id):
    with open('alpha_missense.tsv') as f:
        for line in f:
            if line.startswith(uniprot_id):
                print(line)
                fields = line.strip().split('\t')
                if mutation_id == fields[1]:
                    return fields[2], fields[3]
    return None, None

print(get_alphamissense_result('P43235', '1BY8'))