import dspy


class Search(dspy.Signature):
    """Extract if the given search result content contains call for paper information of a given conference and year"""

    conference: str = dspy.InputField(
        desc="The name of the conference, e.g. NeurIPS, ICML, NSDI, ASPLOS"
    )
    year: int = dspy.InputField(desc="The year of the conference, e.g. 2023, 2024")
    search_result: str = dspy.InputField(desc="Google search result text content")
    has_cfp: bool = dspy.OutputField(
        desc="Whether the given results contains call for paper information of the given conference and year"
    )
    cfp_link: str = dspy.OutputField(
        desc="The link to the call for paper page of the given conference and year, empty string if not found"
    )
