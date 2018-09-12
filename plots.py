import pandas as pd
import seaborn as sns
sns.set(style="ticks")

df = pd.read_csv('input1.csv', names=['X', 'Y', 'Class'])
g = sns.pairplot(df, hue='Class', vars=['X','Y'])
g.savefig('dataset1.png')

df = pd.read_csv('input2.tsv', sep='\t', names=['X', 'Y', 'Class'])
g = sns.pairplot(df, hue='Class', vars=['X','Y'])
g.savefig('dataset2.png')
