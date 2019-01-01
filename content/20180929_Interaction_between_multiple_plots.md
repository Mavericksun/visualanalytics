Title: Interaction between multiple plots
Date: 2018-09-29 15:35
Category: internal
Slug: Interaction_between_multiple_plots
Authors: Sun Yuanjing

#### The plots is from [Fan Power anomaly detection](http://172.28.203.127:9001/Fan-power-anomaly-detection.html) 
Jupyter notebook can be download in the link. Chrome browser is recommended for interactive plot display. If the notebook cannot display interactive plot without warning error message, check the browser first.
<span><img src="{filename}/static/fan_power_associate.gif"  width="80%"></span>

#### Packages
Make sure your UTCDAL version is 1.1.1.  If not, refer to [installation guide](http://172.28.203.93/DBI-DAL/UTCDAL/wikis/2.-Installation-guide#installing-dal)

```python
import pandas as pd
import numpy as np
from UTCDAL.Design.TimeseriesAnalysis import features, extract_features
import altair as alt
alt.renderers.enable('notebook')
%matplotlib inline
%load_ext autoreload
%autoreload 2
```


#### Data frames
Export Controlled: ECCN EAR1E998

Warning: This document contains technical data whose export is restricted by the Bureau of Industry & Security’s Export Administration Regulations and cannot be exported or re-exported without the authorization of the U.S. government. Violations of these export laws are subject to severe criminal penalties. Diversion contrary to U.S. law is prohibited.

*Click [this]({filename}/ipynbs/data-for-Fan-power-anomaly-detection.zip) to download test data.*

#### Domain background and chart type advantage

#### Customizing features

#### Reference