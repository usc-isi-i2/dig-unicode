dig-unicode
===========

Inferlink (Java) and ISI (python) code to build feature rep of unicode chars


Python portion (philpot)

12 December 2014
for each of {body, title}:
  the unicodeSignature is the sequence of >ascii codepoints, in order, space-separated
  the unicodeCatalog is the bag of >ascii codepoints, sorted/agglomerated using space, comma-separated
  the unicodeHistogram is a json-encoded python dict/json object mapping codepoint to count

  the unicodeBlockSignature is the sequence of block descriptors (of all >ascii), in order, space-separated
  the unicodeBlockCatalog is the bag of block descriptors, sorted/agglomerated using space, comma-separated
  the unicodeBlockHistogram is a json-encoded python dict/json object mapping block descriptor to count

  the unicodeCategorySignature is the sequence of category descriptors (of all >ascii), in order, space-separated
  the unicodeCategoryCatalog is the bag of category descriptors, sorted/agglomerated using space, comma-separated
  the unicodeCategoryHistogram is a json-encoded python dict/json object mapping category descriptor to count

  where block and category descriptors are defined via
    # From http://stackoverflow.com/a/245072
    # retrieved from http://unicode.org/Public/UNIDATA/Blocks.txt
    # Blocks-5.1.0.txt
    # Date: 2008-03-20, 17:41:00 PDT [KW]
  and is formatted to using _ rather than ,/space/-e