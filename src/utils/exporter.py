import csv

def export_sentence_pairs(pairs, output_path='data/sbert_training_pairs.csv'):
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['sentence1', 'sentence2', 'score'])
        for sent1, sent2, score in pairs:
            writer.writerow([sent1, sent2, score])
