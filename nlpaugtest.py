import nlpaug.augmenter.word as naw

aug = naw.SynonymAug(aug_src='wordnet')

text = 'On 20250320 at 125232, user DDIC from client 800 successfully logged on using type B and method A on system w16s24id8606.'
augmented_text = aug.augment(text)
print('Original:', text)
print('Augmented:', augmented_text)