"""Show enhanced uncertainty and temporal gate outputs."""

from surgul.gates_enhanced import Gate_G5_Enhanced, Gate_G6_Enhanced


def main() -> None:
    patient = {
        "age": 70,
        "onset_hours": 3,
        "pattern": "worsening",
        "timing": "acute",
        "HINTS_head_impulse": "unknown",
        "HINTS_nystagmus": "unknown",
        "cardiovascular_history": True,
        "hypertension": True,
    }

    uncertainty_output = Gate_G5_Enhanced()(patient)
    temporal_output = Gate_G6_Enhanced()(patient)

    print("G5", uncertainty_output.tier.name, uncertainty_output.explanation)
    print("G6", temporal_output.tier.name, temporal_output.enforcement)


if __name__ == "__main__":
    main()
