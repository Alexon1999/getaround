import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
from utils import generate_pdf

warnings.filterwarnings('ignore')

# to make your app take up all the available space in the browser window
# (not just a single column)
st.set_page_config(layout='wide')


@st.cache
def load_data():
    df = pd.read_excel('get_around_delay_analysis.xlsx')
    return df


@st.cache
def load_pdf_link():
    link = generate_pdf('report.html')
    return link


pdf_link = load_pdf_link()

col1, col2 = st.columns([8, 2])


def export_report():
    col2.markdown(pdf_link, unsafe_allow_html=True)
    st.balloons()


with col2:
    pdf_link = generate_pdf('report.html')
    st.markdown(pdf_link, unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 6, 2])

with col2:
    st.image('https://lever-client-logos.s3.amazonaws.com/2bd4cdf9-37f2-497f-9096-c2793296a75f-1568844229943.png', width=800)


st.markdown("# Introduction")
st.markdown("""
    👋 Hello there! Welcome to our Getaround Web Dashboard.
""")

data_load_state = st.text('Loading data...')
df = load_data()
# change text from "Loading data..." to "" once the the load_data function has run
data_load_state.text("")


# Run the below code if the check is checked ✅
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)

    # Basic stats
    st.markdown("Number of rows : {}".format(df.shape[0]))
    st.markdown("Number of columns : {}".format(df.shape[1]))

st.markdown('# Data Analysis')

# # EDA

# **EDA will help the product Management team with the below Questions :**
#
# - Which share of our owner’s revenue would potentially be affected by the feature
# - How many rentals would be affected by the feature depending on the threshold and scope we choose?
# - How often are drivers late for the next check-in?
# - How does it impact the next driver?
# - How many problematic cases will it solve depending on the chosen threshold and scope?
#
# **Our Product Manager needs to decide:**
#
# - threshold: how long should the minimum delay be?
# - scope: should we enable the feature for all cars?, only Connect cars?
#
# <br />
#
# > ##### So Our Final Goal is to determine the optimal threshold and scope.


st.markdown('## Descriptive analysis')

st.markdown(f"> there are {len(df['car_id'].unique())} unique cars")

tmp = df['checkin_type'].value_counts()
fig = px.pie(values=tmp.values, names=tmp.index,
             title='Proportion of Check-In Type Rentals')
st.plotly_chart(fig, use_container_width=True)

fig = px.histogram(df,
                   x='state',
                   color='state',
                   text_auto='.0f',
                   color_discrete_map={
                       'ended': '#91F5AD', 'canceled': '#FFA69E'},
                   title='Proportion of Rental state')
st.plotly_chart(fig, use_container_width=True)

tmp = df.groupby(by=["state", "checkin_type"]).size().reset_index(name="count")
fig = px.bar(tmp, x="state", y='count', color="checkin_type", barmode="group",
             title='Visualization of Rentals by State and Check-in type', text_auto='.0f')
st.plotly_chart(fig, use_container_width=True)

st.markdown('![purple-divider](https://user-images.githubusercontent.com/7065401/52071927-c1cd7100-2562-11e9-908a-dde91ba14e59.png)')

st.markdown('## Exploratory Analysis')

st.markdown(""" 
**Details about Columns**:

>  ```delay_at_checkout_in_minutes``` This column is referring to the time it takes for the customer to return the car after the agreed-upon rental end time, this column would represent the amount of time that the car was returned late. If the value in the "delay at checkout in minutes" column is negative (e.g. -21), this would indicate that the customer returned the car before the agreed-upon rental end time.

> ```time_delta_with_previous_rental_in_minutes``` : This column records the time difference in minutes between the end of the previous rental and the start of the current rental for the same car.

""")

st.markdown('')
st.markdown("""
### **What is the typical/center time before the next rental ?**
""", unsafe_allow_html=True)

min_time_rental = df['time_delta_with_previous_rental_in_minutes'].min()
max_time_rental = df['time_delta_with_previous_rental_in_minutes'].max()
mean_time_rental = df['time_delta_with_previous_rental_in_minutes'].mean()
median_time_rental = df['time_delta_with_previous_rental_in_minutes'].median()

st.markdown(f"""
Min/Max/Mean/Median time needed for the owner to rent again a car :

| Min | Max  | Mean  |  Median |
|---|---|---|---|
| {min_time_rental}  | {max_time_rental}  | { mean_time_rental}  |  { median_time_rental} |

<br />
""", unsafe_allow_html=True)

fig = px.histogram(df,
                   x='time_delta_with_previous_rental_in_minutes',
                   title='Distribution of time_delta_with_previous_rental_in_minutes'
                   )
fig.add_vline(x=mean_time_rental, line_width=3, line_dash="dash",
              line_color="black", annotation_text='mean')
fig.add_vline(x=median_time_rental, line_width=3, line_dash="dash",
              line_color="red", annotation_text='median')
st.plotly_chart(fig, use_container_width=True)

st.markdown(""" 
This type of distribution is called a right-skewed or positive-skewed distribution. In situations where the data is not normally distributed, it may be more appropriate to use the median instead of the mean as a measure of central tendency.

> The typical value for the next rental is **<font color="#5FBA7C">3 hours</font>** (180 minutes).

<br />

### **Will the vehicle be rented immediately?**
""", unsafe_allow_html=True)

# Rental Ended
df_delay_rented = df.dropna(subset='delay_at_checkout_in_minutes').copy()

list_to_add = []

for value in df_delay_rented['time_delta_with_previous_rental_in_minutes']:
    if value >= 0.0 and value <= 180.0:
        list_to_add.append('time delta btw 0 and 3 hours')
    else:
        list_to_add.append('time delta > 3 hours')

df_delay_rented['time_delta_previous_rental_label'] = list_to_add

df_delay_rented['time_delta_previous_rental_label'].value_counts(
    normalize=True)

fig = make_subplots(rows=1, cols=2, column_widths=[0.6, 0.4], specs=[
                    [{'type': 'domain'}, {'type': 'xy'}]])

labels = 'rented later than 3 hours', 'rented less than 3 hours'
fig.add_trace(
    go.Pie(
        values=df_delay_rented['time_delta_previous_rental_label'].value_counts(
        ),
        labels=labels,
        title='Proportion of cars rented later than 3 hours'
    ),
    row=1, col=1
)

fig.add_trace(
    go.Histogram(x=df_delay_rented['time_delta_previous_rental_label']),
    row=1, col=2
)

fig.update_layout(
    height=600,
    width=1300,
    margin=dict(r=10, t=25, b=40, l=60)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
> Only **<font color="#5FBA7C">5%</font>** of the vehicles are rented again in between **0 - 3 hours**.

<br />

### **How far drivers are late at checkout?**
""", unsafe_allow_html=True)

# Rental Ended
df_checkout = df.dropna(subset='delay_at_checkout_in_minutes').copy()

df_checkout['checkout_status'] = df_checkout['delay_at_checkout_in_minutes'].apply(
    lambda x: 'out_of_time' if x >= 0 else 'in_time')

tmp = df_checkout['checkout_status'].value_counts()
fig = px.pie(values=tmp.values, names=tmp.index,
             title='Proportion of Checkout Status')
st.plotly_chart(fig, use_container_width=True)

fig = px.histogram(df_checkout, x='delay_at_checkout_in_minutes', range_x=(-800, 800),
                   title='Distribution of delay_at_checkout_in_minutes ')
st.plotly_chart(fig, use_container_width=True)

# The majority of the delay within checkout distribution is between **-200** and **200** minutes

fig = px.box(df_checkout, y="delay_at_checkout_in_minutes",
             range_y=(-15000, 15000))
st.plotly_chart(fig, use_container_width=True)

st.markdown(f"""
Description of ```delay_at_checkout_in_minutes```
| Min | Max  | Mean  |  Median |
|---|---|---|---|
| {df_checkout['delay_at_checkout_in_minutes'].min()}  | {df_checkout['delay_at_checkout_in_minutes'].max()}  | { df_checkout['delay_at_checkout_in_minutes'].mean()}  |  { df_checkout['delay_at_checkout_in_minutes'].median()} |

<br />
""", unsafe_allow_html=True)

st.markdown(""" 
> In general, Drivers return the vehicules with **<font color="#5FBA7C">1 hour delay</font>**.

<br />

### **How this late impact the next driver**
""", unsafe_allow_html=True)

all_cancelations = df.loc[(df['state'] == 'canceled')]
cancelations_affected_by_previous_rental = df.loc[(
    df['state'] == 'canceled') & (~df['previous_ended_rental_id'].isna())]

cancelation_desc = pd.DataFrame([[all_cancelations.shape[0], 'all_cancelations'], [
                                cancelations_affected_by_previous_rental.shape[0], 'cancelations_affected_by_previous_rental']], columns=['count', 'state'])

fig = px.bar(cancelation_desc, x='state', y='count', color='state',
             title='Description of Cancelation', text_auto='.0f')
st.plotly_chart(fig, use_container_width=True)

st.markdown(""" 
> #### So 3265 - 229 = 3036 , so we don't know the reasons why <font color="red">3036</font> rentals are canceled.
""", unsafe_allow_html=True)

df_canceled = df.loc[(df['state'] == 'canceled') & (
    ~df['previous_ended_rental_id'].isna())]

df_canceled = df_canceled.merge(right=df, how='left', left_on='previous_ended_rental_id',
                                right_on='rental_id', suffixes=(None, '_previous'))

df_canceled['checkout_status_previous'] = df_canceled['delay_at_checkout_in_minutes_previous'].apply(
    lambda x: 'out_of_time' if x > 0 else 'in_time')

tmp = df_canceled['checkout_status_previous'].value_counts()
fig = px.pie(values=tmp.values, names=tmp.index,
             title='Previous late checkouts')
st.plotly_chart(fig, use_container_width=True)


st.markdown(""" 
> #### Reasons Why the next driver cancel the rental ?
""", unsafe_allow_html=True)

# keeps only the delays and sets the other values to 0,
# otherwise we set previous early checkouts to 0 and keeps late checkouts.
df_canceled['delay_at_checkout_with_previous_rental'] = df_canceled['delay_at_checkout_in_minutes_previous'].apply(
    lambda x: x if x > 0 else 0)

# calculate the delay at checkin
df_canceled['delay_at_checkin_in_minutes'] = df_canceled['delay_at_checkout_with_previous_rental'] - \
    df_canceled['time_delta_with_previous_rental_in_minutes']

# create a new feature : delay_checkin yes or no
df_canceled['delay_checkin'] = df_canceled['delay_at_checkin_in_minutes'].apply(
    lambda x: "yes" if x > 0 else "no")

tmp = df_canceled['delay_checkin'].value_counts()
fig = px.pie(values=tmp.values, names=['other_reasons', 'previous_driver_late'], title='Proportion of Delay Checkin', color_discrete_map={
             'no': '#91F5AD', 'yes': '#FFA69E'}, color=tmp.index)
st.plotly_chart(fig, use_container_width=True)

st.markdown(""" 
> #### We can say that because the previous driver is in late for the checkout, the next driver will cancel it.
> ##### There are <font color='red'>37 cancelations</font> that are coming from late checkouts.
> ##### There are <font color='red'>192 cancelations</font> with the reasons we can't explain. it's something we have to investigate with the owners because this is nothing to do with the late.

- #### threshold of 3 hours
""", unsafe_allow_html=True)


st.markdown(""" 
> ##### There are <font color='green'>31 cancelations so 83% of cancelations from late checkouts</font> could be prevent if we put a threshold of 3 hours.

<br />

### Should we enable the feature for all cars?, only Connect cars?
""", unsafe_allow_html=True)

df_checkout_late = df_checkout[df_checkout['checkout_status'] == 'out_of_time']

list_to_add = []

for value in df_checkout_late['delay_at_checkout_in_minutes']:
    if value > 0.0 and value <= 60.0:
        list_to_add.append('late <= 1 hour')
    elif value > 60.0 and value <= 120.0:
        list_to_add.append('late btw 1 and 2 hours')
    elif value > 120.0 and value <= 180.0:
        list_to_add.append('late btw 2 and 3 hours')
    elif value > 180.0 and value <= 240.0:
        list_to_add.append('late btw 3 and 4 hours')
    elif value > 240.0 and value <= 360:
        list_to_add.append('late btw 4 and 6 hours')
    elif value > 360 and value <= 1440.0:                   # 24 * 60.0 = 1440, 1 day
        list_to_add.append('late btw 6h and 1 day')
    elif value > 1440.0 and value <= 2880.0:                # 2 days
        list_to_add.append('late btw 1 and 2 days')
    elif value > 2880.0 and value <= 4320.0:                # 3 days
        list_to_add.append('late btw 2 and 3 days')
    elif value > 4320.0 and value <= 5760.0:                # 4 days
        list_to_add.append('late btw 3 and 4 days')
    elif value > 4320.0 and value <= 7200.0:                # 5 days
        list_to_add.append('late btw 4 and 5 days')
    elif value > 7200.0 and value <= 8640.0:                # 6 days
        list_to_add.append('late btw 5 and 6 days')
    elif value > 8640.0 and value <= 10080.0:               # 7 days
        list_to_add.append('late btw 6 and 7 days')
    elif value > 10080.0 and value <= 11520.0:              # 8 days
        list_to_add.append('late btw 7 and 8 days')
    elif value > 11520.0 and value <= 12960.0:              # 9 days
        list_to_add.append('late btw 8 and 9 days')
    elif value > 12960.0 and value <= 14400.0:              # 10 days
        list_to_add.append('late btw 9 and 10 days')
    else:
        list_to_add.append('late more than 10 days')

df_checkout_late['late_groups'] = list_to_add

tmp_all_checkin = df_checkout_late['late_groups'].value_counts()

tmp_connect = df_checkout_late.loc[df_checkout_late['checkin_type']
                                   == 'connect', 'late_groups'].value_counts()

fig = go.Figure()

fig.add_trace(go.Bar(
    y=tmp_connect.index,
    x=tmp_connect.values,
    name='Count Late groups / Connect checkin rentals',
    orientation='h',
    marker=dict(
        color='rgba(58, 71, 80, 0.6)',
        line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
    ),
))

fig.add_trace(go.Bar(
    y=tmp_all_checkin.index,
    x=tmp_all_checkin.values,
    name='Count Late groups / All checkin rentals',
    orientation='h',
    marker=dict(
        color='rgba(246, 78, 139, 0.6)',
        line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
    ),
))

fig.update_layout(barmode='group', height=800)
st.plotly_chart(fig, use_container_width=True)


st.markdown(""" 
> if we choose the minimum delay of 3 hours for the next rental, **we should enable the fearure for <font color='#5FBA7C'>all cars</font>**.

<br />

### How many problematic cases will it solve depending on the chosen threshold and scope?

> The feature realized with a threshold of 3 hours on all cars / checkin types
""", unsafe_allow_html=True)

list_to_add = []

for value in df_checkout_late['delay_at_checkout_in_minutes']:
    if value > 0.0 and value <= 180.0:
        list_to_add.append(True)
    else:
        list_to_add.append(False)

df_checkout_late['solved'] = list_to_add

tmp = df_checkout_late['solved'].value_counts()
fig = px.pie(values=tmp.values, names=tmp.index,
             title='Proportion of Solved Cases with a threshold of 3 hours on all cars / checkin types')
st.plotly_chart(fig, use_container_width=True)

st.markdown(""" 
> The feature realized with a threshold of 3 hours on all cars / checkin types should solve almost <font color="#5FBA7C">7679</font> problematic cases.
""", unsafe_allow_html=True)

# # Conclusion

# - The feature might be realized with a thresold of 3 hours (on all cars / checkin types)
# - Only about 5% of this part of rented cars might have a negative impact on global revenues
# - Most of cars are rented again with after 3 hours
# - In general, Drivers return the vehicules with 1 hour delay so the late leads to cancelation.
# - But with a threshold of 3 hours, we can prevent 83% of cancelations from late checkouts.
# - ~3000 rentals are canceled and we don't know the reason behind it.
# - A cancel time feature can help us to see how long waiting time leads customers to cancel the rental.
# - This feature should solve almost 7679 problematic cases.
