#importing dependecies
import pandas as pd
import streamlit as st
import plotly.express as px
import sqlalchemy as sal
from sqlalchemy import create_engine
#from urllib.request import urlopen
import json
#configuring default setting of the page 
st.set_page_config(layout ="wide") 
#creating connection to mysql DB
def main():
    try:
        host = 'localhost'
        user='root'
        password='root'
        db_name='phonepe'
        port = '3306'
        #creating a db connection with values mentioned
        def get_connection():
            #con = sal.create_engine(‘dialect+driver://username:password@host:port/database’)
            return sal.create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}'.
                                format(user=user,password=password,host=host,port=port,db_name=db_name
                                    )
                            )
        eng = get_connection()
    except:
        pass
    
    st.title("_:red[Phonepe Pulse Data Analysis]_")
    tb1,tb2,tb3,tb4= st.tabs(['Geographic Visualization','Transaction Analysis','User Analysis','Top Analysis'])
    
    with tb1:
        col1, col2 = st.columns(2)
        with col1:
            #selecting the year
            Year = ['2022','2021','2020','2019','2018']
            ys = st.selectbox("Select Year", Year,key='Year')
            #selecting the quarter
        with col2: 
            Quarter = ['1','2','3','4']
            Quarter_selected = st.selectbox("Select Quarter", Quarter)
            qs = int(Quarter_selected)
        st.write("")

        col1,col2 = st.columns(2)
        with col1:    
            agg_transaction_df= pd.read_sql("select * from agg_transaction where year={} and quarter = {}".format(ys,qs), eng)
            #agg_transaction_df
            agg_transaction_df['transaction_amount'] = agg_transaction_df['transaction_amount'].astype(int)
            #choropleth map to make india map. geojson file contains geometry information of indian states
            fig = px.choropleth(agg_transaction_df,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            locations="state",
                            featureidkey = "properties.ST_NM",
                            color = agg_transaction_df['transaction_amount'],
                            color_continuous_scale="Viridis",
                            scope='asia',
                            hover_name = 'state',
                            hover_data = ['transaction_amount', 'transaction_count','year','quarter']
                        )
            #hiding the base map frame by assigning visible to false, 
            fig.update_geos(fitbounds="locations",visible=False )
            fig.update_layout(height=500,width=700)
            st.subheader(":blue[Geographical Visualization]")
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.subheader(":blue[Transactions]")
            st.write("**:green[Total Phonepe payment value]**") 
            tot_trans = pd.read_sql("select sum(transaction_amount) as Total_Transaction_Amount from agg_transaction where year={} and quarter = {}".format(ys,qs), eng)         
            st.write(tot_trans['Total_Transaction_Amount'])
            st.write("**:green[Categories]**")
            type_tot_transaction = pd.read_sql("select transaction_type , sum(transaction_amount) as Transaction_Amount from agg_transaction where year={} and quarter = {} group by transaction_type".format(ys,qs), eng)
            st.dataframe(type_tot_transaction,use_container_width=True)
            #st.subheader(" **:blue[Map shows the different transction amount in each state with color intensity variation based on the selected year and quarter]**")
            #st.write(":red[Darker the color, higher the transaction amount]")
            
        #plotting the bar chart for the state and transaction count
        st.subheader(":green[Bar Chart Analysis for Total Transaction count in Various State for the selected year and quarter]")
        #st.write(":red[Double Click on transaction type to view bar chart for individual transactiont type ]")
        st.write('**Overall Transaction**')
        
        agg_transaction_df['transaction_count'] = agg_transaction_df['transaction_count'].astype(int)
        agg_transaction_df_sort = agg_transaction_df.sort_values(by=['transaction_count'],ascending=False)
        fig = px.bar(agg_transaction_df_sort,
                     x='state', y='transaction_count',
                     #color=agg_transaction_df["transaction_type"],
                     #legend_name = 'Transaction Type',
                     title="Bar chart analysis")
        st.plotly_chart(fig,use_container_width=True)
    
    with tb2:

        tb21,tb22,tb33= st.tabs(['State analysis','District Analysis','Total'])
        with tb21:
            col1,col2 = st.columns(2)
            with col1:
                State = ['Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                'Dadra And Nagar Haveli And Daman And Diu', 'Delhi', 'Goa',
                'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                'Uttarakhand', 'West Bengal']
                ss = st.selectbox("Select State",State,key='state')
            with col2:
                Transactiontype = ['Recharge & bill payments','Peer-to-peer payments','Merchant payments','Financial Services','Others']
                sel_ttype = st.selectbox("Select Transaction Type",Transactiontype)
            #st.write(ss)
            #st.write(sel_ttype)
                df1 = pd.read_sql("select year,quarter,transaction_count,transaction_type from agg_transaction where state='{}' and transaction_type='{}'".format(ss,sel_ttype),eng)
                df1['year_quarter'] = df1['year']+'-'+'Q'+df1['quarter'].astype(str)
            st.write()
            col1,col2 = st.columns([5,3],gap='large')
            with col1:
                st.subheader(":blue[Bar chart analysis of transaction count for particular category in each quarter in a year from 2018 - 2022]")
                fig1 = px.bar(df1,x='year_quarter',y='transaction_count',color='transaction_count',color_continuous_scale="Turbo") 
                st.plotly_chart(fig1,use_container_width=True)  
            with col2:
                dfamount = pd.read_sql("select year,quarter,transaction_amount as Total_Transaction_Value from agg_transaction where state='{}' and transaction_type='{}'".format(ss,sel_ttype),eng)
                st.subheader(":blue[Total Transaction Values]")
                st.write(dfamount)
        with tb22:
            col1,col2 = st.columns(2)
            with col1:
                St = ['Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                'Dadra And Nagar Haveli And Daman And Diu', 'Delhi', 'Goa',
                'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                'Uttarakhand', 'West Bengal']
                sels = st.selectbox("Select State",St,key='st')
            with col2:
                Yea = ['2022','2021','2020','2019','2018']
                sely = st.selectbox("Select Year", Yea,key="yea")
                dfdist = pd.read_sql("select * from map_transaction where state='{}' and year='{}'".format(sels,sely),eng)
            col1,col2 = st.columns([5,3],gap='large')
            with col1:
                st.subheader(":blue[Bar chart analysis of all transaction in district level of {}]".format(sels))
                fig1 = px.bar(dfdist,x='district',y='transaction_metric_count',color="transaction_metric_amount",color_continuous_scale="Viridis") 
                st.plotly_chart(fig1,use_container_width=True)  
            with col2:
                dfdistamount = pd.read_sql("select district,sum(transaction_metric_amount) as Total_Transaction_Value from map_transaction where state='{}' and year='{}' group by district".format(sels,sely),eng)
                st.subheader(":blue[Total Transaction Values of districts in {} ]".format(sels))
                dfdistamount['Total_Transaction_Value'] = round(dfdistamount['Total_Transaction_Value'],2)
                st.markdown(dfdistamount.style.hide(axis='index').to_html(),unsafe_allow_html=True)
        with tb33:
            Sta = ['Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                'Dadra And Nagar Haveli And Daman And Diu', 'Delhi', 'Goa',
                'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                'Uttarakhand', 'West Bengal']
            sels = st.selectbox("Select State",Sta,key='sta')
            st.subheader("Phonepe Transactions in each year - {}".format(sels))
            dfyear = pd.read_sql("select * from agg_transaction where state='{}'".format(sels),eng)
            fig = px.sunburst(dfyear,path=['year','quarter','transaction_type'],values='transaction_count')
            fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))


           # fig.update_traces(textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
    with tb3:
        tb31,tb32,tb33 = st.tabs(['Users by brand','District and State analysis','Overall analysis'])
        with tb31:
            col1, col2 = st.columns(2,gap='large')
            with col1:
                #selecting the year
                Year = ['2022','2021','2020','2019','2018']
                ys = st.selectbox("Select Year", Year,key='Yearuser')
                #selecting the quarter
            with col2: 
                State = ['Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                    'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                    'Dadra And Nagar Haveli And Daman And Diu', 'Delhi', 'Goa',
                    'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                    'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                    'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                    'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                    'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                    'Uttarakhand', 'West Bengal']
                ss = st.selectbox("Select State",State,key='stateuser')
            dfuser = pd.read_sql("select * from agg_user where state='{}' and year = '{}'".format(ss,ys),eng)
            dfuser['percentage'] = dfuser['percentage']*100
            dfuser['percentage'] = dfuser['percentage'].astype(str)+"%"
            dfuser['brand_share'] = dfuser['brand'] +' - '+dfuser['percentage']
            fig = px.bar(dfuser, y='brand',x='user_count',color="brand_share",
                         title="User count by brands and brand share",
                         )
            st.plotly_chart(fig,use_container_width=True)
        with tb32:
            State = ['Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                    'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                    'Dadra And Nagar Haveli And Daman And Diu', 'Delhi', 'Goa',
                    'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                    'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                    'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                    'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                    'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                    'Uttarakhand', 'West Bengal']
            ss = st.selectbox("Select State",State,key='distuser')
            Year = ['2022','2021','2020','2019','2018']
            ys = st.selectbox("Select Year", Year,key='distYear')
            dfdist = pd.read_sql("select * from map_users where state='{}' and year='{}'".format(ss,ys),eng)
            co1,co2 = st.columns([2,1])
            with co1:
                fig = px.bar(dfdist, y='registered_users',x='district',
                            title="{} - User count bar chart - district wise - {}".format(ys,ss),
                            )
                st.plotly_chart(fig,use_container_width=True)
            with co2:
                dfdist1 =pd.read_sql("select district,registered_users from map_users where state='{}' and year='{}'".format(ss,ys) ,eng)
                st.write("**:blue[{} - User count by district wise - {}]**".format(ys,ss))
                st.dataframe(dfdist1)
                fig.update_layout(height=700,width=700)

            with tb33:
                co1,co2 = st.columns([4,2],gap='medium')
                with co1:
                    State = ['Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                    'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                    'Dadra And Nagar Haveli And Daman And Diu', 'Delhi', 'Goa',
                    'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                    'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                    'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                    'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                    'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                    'Uttarakhand', 'West Bengal']
                    ss = st.selectbox("Select State",State,key='overalluser')
                    sumuserdf =pd.read_sql("select year, state,sum(registered_users) as Registered_Users,sum(appopens) as App_opens from sum_agg_user where state='{}' group by year,state".format(ss),eng)
                    fig = px.bar(sumuserdf,y=sumuserdf['year'],x = 'Registered_Users', barmode = 'group',color= 'App_opens',title="Bar ananlysis")
                    #fig = px.bar(sumuserdf,y=sumuserdf['year'],x ='App_opens',barmode = 'group')#marker={'color': 'green'})
                    st.plotly_chart(fig,use_container_width=True)
                with co2: 
                    st.write(':green[Total no of phonepe users and app opens per year]')   
                    st.write(sumuserdf)
    with tb4:
        Year = ['2022','2021','2020','2019','2018']
        ys = st.selectbox("Select Year", Year,key='Yeartop')
        col41,col42 = st.columns(2,gap="medium")
        with col41:
            st.write("**:blue[Top 10 states with maximum Phonpe transactions in year {}]**".format(ys))
            topstate = pd.read_sql("select state,sum(transaction_count) as Total_Phonepe_Transaction from agg_transaction where year={} group by state order by Total_Phonepe_Transaction desc".format(ys),eng)
            st.write(topstate.head(10))
        with col42:
            st.write("**:blue[Top 10 states with maximum phonepe users in year {}]**".format(ys))
            topuser  = pd.read_sql("select state, sum(registered_users) as Total_Phonepe_Users from sum_agg_user where year ={} group by state order by Total_Phonepe_Users desc ".format(ys),eng)
            st.write(topuser.head(10))
    

                    

main()
