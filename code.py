import os
import re
import numpy as np
from scipy import stats

def parse_custom_conll(file_path):
    sentences_data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        current_sent = []
        for line in f:
            line = line.strip()
            if not line:
                if current_sent:
                    sentences_data.append(current_sent)
                    current_sent = []
                continue
            
            columns = re.split(r'\t| {2,}', line)
            
            if len(columns) >= 8:
                try:
                    token = {
                        'id': int(columns[0]),
                        'head': int(columns[6]) if columns[6].isdigit() else 0,
                        'deprel': columns[7],
                        'feats': columns[5]
                    }
                    current_sent.append(token)
                except (ValueError, IndexError):
                    continue 
        if current_sent:
            sentences_data.append(current_sent)
    return sentences_data

def analyze_treebank(base_path, is_folder=True):
    distances = []
    rel_counts = {}
    feature_counts = {}

    files_to_process = []
    if is_folder:
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.endswith(".dat") or file.endswith(".conll"):
                    files_to_process.append(os.path.join(root, file))
    else:
        files_to_process.append(base_path)

    for file_path in files_to_process:
        sentences = parse_custom_conll(file_path)
        for sent in sentences:
            for token in sent:
                if token['head'] > 0:
                    distances.append(abs(token['id'] - token['head']))
                
                rel = token['deprel']
                rel_counts[rel] = rel_counts.get(rel, 0) + 1
                
                if token['feats'] and token['feats'] != '_':
                    parts = token['feats'].split('|')
                    for p in parts:
                        if '-' in p:
                            feat_name = p.split('-')[0]
                            feature_counts[feat_name] = feature_counts.get(feat_name, 0) + 1
                            
    return distances, rel_counts, feature_counts

hindi_path = "CoNLL/utf"
telugu_file = "iiit_hcu_intra_chunk_v1.conll"

h_dist, h_rel, h_morph = analyze_treebank(hindi_path, is_folder=True)
t_dist, t_rel, t_morph = analyze_treebank(telugu_file, is_folder=False)

if h_dist and t_dist:
    t_stat, p_val = stats.ttest_ind(h_dist, t_dist)
    print(f"Hindi Mean: {np.mean(h_dist):.2f} | Hindi Median: {np.median(h_dist)}")
    print(f"Telugu Mean: {np.mean(t_dist):.2f} | Telugu Median: {np.median(t_dist)}")
    print(f"Significance: p-value = {p_val:.2f}")
else:
    print("Error: One of the datasets is empty. Check your file paths!")

def print_top_10(counts, lang_name):
    print(f"\nTop 10 Dependency Relations for {lang_name}:")
    sorted_rels = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]
    print(f"{'Relation':<15} | {'Count':<10}")
    print("-" * 28)
    for rel, count in sorted_rels:
        print(f"{rel:<15} | {count:<10}")

print_top_10(h_rel, "Hindi")
print_top_10(t_rel, "Telugu")

def print_morph_features(counts, lang_name):
    print(f"\nTop Morphological Features for {lang_name}:")
    sorted_feats = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for feat, count in sorted_feats:
        print(f"{feat}: {count}")

print_morph_features(h_morph, "Hindi")
print_morph_features(t_morph, "Telugu")