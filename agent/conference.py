import dspy


class Conference(dspy.Signature):
    """Extract conference information from a given cfp html content"""

    html: str = dspy.InputField()
    title: str = dspy.OutputField(
        desc="Conference title, e.g. NeurIPS, ICML, NSDI (Spring), ASPLOS (Fall)"
    )
    year: int = dspy.OutputField(desc="The year conference is held, e.g. 2023, 2024")
    id: str = dspy.OutputField(
        desc="A unique string ID for the conference, e.g. neuroips-2023, icml-2024, nsdi-2024-spring"
    )
    paper_deadline: str = dspy.OutputField(
        desc="The paper submission deadline in YYYY-MM-DD HH:mm:ss format"
    )
    abstract_deadline: str = dspy.OutputField(
        desc="The abstract submission deadline in YYYY-MM-DD HH:mm:ss format"
    )
    timezone: str = dspy.OutputField(
        desc="The UTC timezone of the conference deadlines, e.g. UTC-8, UTC+1"
    )
    place: str = dspy.OutputField(
        desc="The location of the conference, e.g. `Renton, WA, USA`,  `Edinburgh, UK`, `Virtual`"
    )
    date: str = dspy.OutputField(
        desc="The date(s) when the conference is held, e.g. `Dec 10-15, 2023`, `June 02-05, 2024`"
    )
    start: str = dspy.OutputField(
        desc="The start date of the conference in YYYY-MM-DD format"
    )
    end: str = dspy.OutputField(
        desc="The end date of the conference in YYYY-MM-DD format"
    )
    sub: str = dspy.OutputField(
        desc="The subject area of the conference out of NET, OS, ML, SS. Map as follows: Networking -> NET, Operating Systems -> OS, Machine Learning -> ML, Storage -> SS"
    )
