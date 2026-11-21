# Regular expression & set difference

Instead of scanning operators in a loop, this version uses a single compiled regular expression (`re.compile`) to extract the package name, optional `[extras]`, operator, and version in one step, and uses set difference (`req_set - inst_set`) in `missing_packages`. Both approaches produce identical results; the loop version is easier for beginners to read, while the regex version scales well when adding more PEP 508 syntax later.
