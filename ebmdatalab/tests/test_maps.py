from ebmdatalab import maps
import tempfile
import pandas as pd


def test_maps():
    """This test just tests nothing fails at the moment
    """
    df = pd.DataFrame(
        [
            ["99P", 0.3],
            ["13T", 1.2]
        ], columns=['pct', 'val'])
    plt = maps.ccg_map(df, title="foo", column='val')
    with tempfile.NamedTemporaryFile() as f:
        plt.savefig(
            f.name,
            format='png',
            dpi=300,
            bbox_inches='tight')
