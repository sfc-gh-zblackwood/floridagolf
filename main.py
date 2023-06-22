
import pandas as pd
import plotly_express as px
import streamlit as st
import time
from PIL import Image


image = Image.open('florida.png')
imgtab = Image.open('gatorlogo.png')

st.set_page_config(page_title='Florida Golf',page_icon=imgtab,layout='wide')

st.sidebar.image(image)

#login

password = st.sidebar.text_input('Password',type='password')
if st.sidebar.checkbox('Log in'):
  if password == 'florida123':
    container = st.empty()
    container.success('Logged in')
    time.sleep(1)
    container.empty()
    
    df=pd.read_csv('forcedecks-test-export-06_21_2023.csv', parse_dates=["Date"])

    #remove columns and change date
    df_updated=df.drop(['ExternalId','Test Type','Time','BW [KG]','Reps','Tags','Additional Load [lb]'], axis=1)
    df_updated['Date'] = pd.to_datetime(df['Date']).dt.date
   
    #sidebar

    st.sidebar.header('Navigation')
    options = st.sidebar.radio('Dashboards:', options=['Readiness', 'Performance','Interactive Graphs','Assymetries', 'Leaderboard', 'Benchmarks', 'All Data'])    
    

    name = st.sidebar.multiselect(
        "Select the Athlete:",
        options=df_updated["Name"].unique(),
        default=df_updated["Name"].unique(),
    )
    
    date_start = st.sidebar.selectbox(
        "Date From:",
        options=df_updated["Date"].unique(),
        index=15
    )

    date_end = st.sidebar.selectbox(
        "Date To:",
        options=df_updated["Date"].unique(),
        index=0
    )
    
    
    
    df_selection = df_updated.query(
        "Date >= @date_start and Date <= @date_end & Name ==@name "
    )

    df_selection1= df_updated.query(
        "Date >= @date_start and Date <= @date_end"
    )
    #Date

    
    

    # TOP KPI's Readiness
    eccentric_duration = int(df_selection["Eccentric Duration [ms] "].mean())
    eccentric_duration_team_avg = int(df_selection1["Eccentric Duration [ms] "].mean())
    ecc_peak_velocity = round(df_selection["Eccentric Peak Velocity [m/s] "].mean(),2)
    ecc_peak_velocity_team_avg = round(df_selection1["Eccentric Peak Velocity [m/s] "].mean(),2)
    cmj_depth = int(df_selection["Countermovement Depth [cm] "].mean())
    cmj_depth_team_avg = int(df_selection1["Countermovement Depth [cm] "].mean())
    ecc_decl_rfd = int(df_selection["Eccentric Deceleration RFD [N/s] "].mean())
    ecc_decl_rfd_team_avg = int(df_selection1["Eccentric Deceleration RFD [N/s] "].mean())
    ecc_decl_imp = int(df_selection["Eccentric Deceleration Impulse [N s] "].mean())
    ecc_decl_imp_team_avg = int(df_selection1["Eccentric Deceleration Impulse [N s] "].mean())
    ecc_peak_force = int(df_selection["Eccentric Peak Force [N] "].mean())
    ecc_peak_force_team_avg = int(df_selection1["Eccentric Peak Force [N] "].mean())
    braking_duration = round(df_selection["Braking Phase Duration [s] "].mean(),2)
    braking_duration_team_avg = round(df_selection1["Braking Phase Duration [s] "].mean(),2)
     

    #Most recent KPI's
    ecc_duration_recent = int(df_selection[df_selection["Date"]==df_selection["Date"].max()]["Eccentric Duration [ms] "].mean())
    ecc_peak_vel_recent = round(df_selection[df_selection["Date"]==df_selection["Date"].max()]["Eccentric Peak Velocity [m/s] "].mean(),2)
    cmj_depth_recent = int(df_selection[df_selection["Date"]==df_selection["Date"].max()]["Countermovement Depth [cm] "].mean())
    ecc_decl_rfd_recent = int(df_selection[df_selection["Date"]==df_selection["Date"].max()]["Eccentric Deceleration RFD [N/s] "].mean())
    ecc_decl_imp_recent = int(df_selection[df_selection["Date"]==df_selection["Date"].max()]["Eccentric Deceleration Impulse [N s] "].mean())
    ecc_peak_force_recent = int(df_selection[df_selection["Date"]==df_selection["Date"].max()]["Eccentric Peak Force [N] "].mean())
    braking_duration_recent = round(df_selection[df_selection["Date"]==df_selection["Date"].max()]["Braking Phase Duration [s] "].mean(),2)

    #calculations for percentages readiness
    ecc_duration_percentage = round(((ecc_duration_recent/eccentric_duration)*100)-100)
    ecc_peak_vel_percentage = round(((ecc_peak_vel_recent/ecc_peak_velocity)*100)-100)
    cmj_depth_percentage = round(((cmj_depth_recent/cmj_depth)*100)-100)
    ecc_decl_rfd_percentage = round(((ecc_decl_rfd_recent/ecc_decl_rfd)*100)-100)
    ecc_decl_imp_percentage = round(((ecc_decl_imp_recent/ecc_decl_imp)*100)-100)
    ecc_peak_force_percentage = round(((ecc_peak_force_recent/ecc_peak_force)*100)-100)
    braking_duration_percentage = round(((braking_duration_recent/braking_duration)*100)-100)
      
    #functions for emojis readiness       
    def ecc_emoji(ecc_duration_percentage): 
      if ecc_duration_percentage < -5:
        return str(ecc_duration_percentage) + " % " + ":fire:"
      elif ecc_duration_percentage > 5:
        return str(ecc_duration_percentage) + " % " + ":exclamation:"
      else:
        return str(ecc_duration_percentage) + " % " + " :thumbsup:"

    def ecc_peak_vel_emoji(ecc_peak_vel_percentage): 
      if ecc_peak_vel_percentage < -5:
        return str(ecc_peak_vel_percentage) + " % " + ":exclamation:"
      elif ecc_peak_vel_percentage >5:
        return str(ecc_peak_vel_percentage) + " % " + ":fire:"
      else:
        return str(ecc_peak_vel_percentage) + " % " + ":thumbsup:"

    def cmj_depth_emoji(cmj_depth_percentage): 
      if cmj_depth_percentage < -5:
        return str(cmj_depth_percentage) + " % " + ":fire:"
      elif cmj_depth_percentage >5:
        return str(cmj_depth_percentage) + " % " + ":exclamation:"
      else:
        return str(cmj_depth_percentage) + " % " + ":thumbsup:"
    
    def ecc_decl_rfd_emoji(ecc_decl_rfd_percentage): 
      if ecc_decl_rfd_percentage < -5:
        return str(ecc_decl_rfd_percentage) + " % " + ":exclamation:"
      elif ecc_decl_rfd_percentage >5:
        return str(ecc_decl_rfd_percentage) + " % " + ":fire:"
      else:
        return str(ecc_decl_rfd_percentage) + " % " + ":thumbsup:"
        
    def ecc_decl_imp_emoji(ecc_decl_imp_percentage): 
      if ecc_decl_imp_percentage < -5:
        return str(ecc_decl_imp_percentage) + " % " + ":exclamation:"
      elif ecc_decl_imp_percentage >5:
        return str(ecc_decl_imp_percentage) + " % " + ":fire:"
      else:
        return str(ecc_decl_imp_percentage) + " % " + ":thumbsup:"
    
    def ecc_peak_force_emoji(ecc_peak_force_percentage): 
      if ecc_peak_force_percentage < -5:
        return str(ecc_peak_force_percentage) + " % " + ":exclamation:"
      elif ecc_peak_force_percentage >5:
        return str(ecc_peak_force_percentage) + " % " + ":fire:"
      else:
        return str(ecc_peak_force_percentage) + " % " + ":thumbsup:"

    def braking_duration_emoji(braking_duration_percentage): 
      if braking_duration_percentage < -5:
        return str(braking_duration_percentage) + " % " + ":fire:"
      elif braking_duration_percentage >5:
        return str(braking_duration_percentage) + " % " + ":exclamation:"
      else:
        return str(braking_duration_percentage) + " % " + ":thumbsup:"
      
    #Graphs readiness

    presentDates=set(df.Date)
    # Set of dates that are missing (the ones in the range of df.Date, but not among the dates)
    missingDates=[d for d in pd.date_range(min(df.Date), max(df.Date), freq='D') if d not in presentDates]  

    #ecc duration graph
    st.write(df_selection)
    ecc_duration_by_name = df_selection.groupby(by=["Date"]).mean(numeric_only=True)[["Eccentric Duration [ms] "]]
    fig_ecc_duration = px.line(
        ecc_duration_by_name,
        x=ecc_duration_by_name.index,
        y="Eccentric Duration [ms] ",
        title="<b>Eccentric Duration</b>",
        color_discrete_sequence=["#3679ff"] * len(ecc_duration_by_name),
        template="plotly_white",
        markers=True
    )
    #adding Average line
    fig_ecc_duration.add_hline(y=eccentric_duration,line_dash="dash", line_color="black", annotation_text="Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="black")
    #adding Team average line
    fig_ecc_duration.add_hline(y=eccentric_duration_team_avg,line_dash="dot", line_color="red", annotation_text="Team Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="red")

    fig_ecc_duration.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=True)),
    )
  
    fig_ecc_duration.update_traces(marker_size=11)
    fig_ecc_duration.update_xaxes(rangebreaks=[dict(values=missingDates)])  #remove empty dates
    
    #ecc peak vel graph
    ecc_peak_vel_by_name = df_selection.groupby(by=["Date"]).mean(numeric_only=True)[["Eccentric Peak Velocity [m/s] "]]
    fig_ecc_peak_vel = px.line(
        ecc_peak_vel_by_name,
        ecc_peak_vel_by_name.index,
        y="Eccentric Peak Velocity [m/s] ",
        title="<b>Eccentric Peak Velocity</b>",
        color_discrete_sequence=["#3679ff"] * len(ecc_peak_vel_by_name),
        template="plotly_white",
        markers=True
    )
    #adding Average line
    fig_ecc_peak_vel.add_hline(y=ecc_peak_velocity,line_dash="dash", line_color="black", annotation_text="Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="black")
    #adding Team average line
    fig_ecc_peak_vel.add_hline(y=ecc_peak_velocity_team_avg,line_dash="dot", line_color="red", annotation_text="Team Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="red")

    fig_ecc_peak_vel.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    fig_ecc_peak_vel.update_traces(marker_size=11)
    fig_ecc_peak_vel.update_xaxes(rangebreaks=[dict(values=missingDates)]) #remove empty dates

    #cmj depth graph
    cmj_depth_by_name = df_selection.groupby(by=["Date"]).mean(numeric_only=True)[["Countermovement Depth [cm] "]]
    fig_cmj_depth = px.line(
        cmj_depth_by_name,
        cmj_depth_by_name.index,
        y="Countermovement Depth [cm] ",
        title="<b>CMJ Depth</b>",
        color_discrete_sequence=["#3679ff"] * len(cmj_depth_by_name),
        template="plotly_white",
        markers=True
    )
    #adding Average line
    fig_cmj_depth.add_hline(y=cmj_depth,line_dash="dash", line_color="black", annotation_text="Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="black")
    #adding team avg line
    fig_cmj_depth.add_hline(y=cmj_depth_team_avg,line_dash="dot", line_color="red", annotation_text="Team Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="red")

    fig_cmj_depth.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    fig_cmj_depth.update_traces(marker_size=11)
    fig_cmj_depth.update_xaxes(rangebreaks=[dict(values=missingDates)])  #remove empty dates
  
    #Eccentric Decl RFD graph
    ecc_decl_rfd_name = df_selection.groupby(by=["Date"]).mean(numeric_only=True)[["Eccentric Deceleration RFD [N/s] "]]
    fig_ecc_decl_rfd = px.line(
        ecc_decl_rfd_name,
        ecc_decl_rfd_name.index,
        y="Eccentric Deceleration RFD [N/s] ",
        title="<b>Eccentric Deceleration RFD</b>",
        color_discrete_sequence=["#3679ff"] * len(ecc_decl_rfd_name),
        template="plotly_white",
        markers=True
    )
    #adding Average line
    fig_ecc_decl_rfd.add_hline(y=ecc_decl_rfd,line_dash="dash", line_color="black", annotation_text="Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="black")
    #adding team Average line
    fig_ecc_decl_rfd.add_hline(y=ecc_decl_rfd_team_avg,line_dash="dot", line_color="red", annotation_text="Team Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="red")

    fig_ecc_decl_rfd.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    fig_ecc_decl_rfd.update_traces(marker_size=11)
    fig_ecc_decl_rfd.update_xaxes(rangebreaks=[dict(values=missingDates)])  #remove empty dates

    #Ecc Decl Impulse graph
    ecc_decl_imp_name = df_selection.groupby(by=["Date"]).mean(numeric_only=True)[["Eccentric Deceleration Impulse [N s] "]]
    fig_ecc_decl_imp = px.line(
        ecc_decl_imp_name,
        ecc_decl_imp_name.index,
        y="Eccentric Deceleration Impulse [N s] ",
        title="<b>Eccentric Decl Impulse</b>",
        color_discrete_sequence=["#3679ff"] * len(ecc_decl_imp_name),
        template="plotly_white",
        markers=True
    )
    #adding Average line
    fig_ecc_decl_imp.add_hline(y=ecc_decl_imp,line_dash="dash", line_color="black", annotation_text="Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="black")
    #adding team Average line
    fig_ecc_decl_imp.add_hline(y=ecc_decl_imp_team_avg,line_dash="dot", line_color="red", annotation_text="Team Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="red")

    fig_ecc_decl_imp.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    fig_ecc_decl_imp.update_traces(marker_size=11)
    fig_ecc_decl_imp.update_xaxes(rangebreaks=[dict(values=missingDates)]) #remove empty dates

    #Ecc peak force graph graph
    ecc_peak_force_name = df_selection.groupby(by=["Date"]).mean(numeric_only=True)[["Eccentric Peak Force [N] "]]
    fig_ecc_peak_force = px.line(
        ecc_peak_force_name,
        ecc_peak_force_name.index,
        y="Eccentric Peak Force [N] ",
        title="<b>Eccentric Peak Force</b>",
        color_discrete_sequence=["#3679ff"] * len(ecc_peak_force_name),
        template="plotly_white",
        markers=True
    )
    #adding Average line
    fig_ecc_peak_force.add_hline(y=ecc_peak_force,line_dash="dash", line_color="black", annotation_text="Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="black")
    #adding team Average line
    fig_ecc_peak_force.add_hline(y=ecc_peak_force_team_avg,line_dash="dot", line_color="red", annotation_text="Team Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="red")

    fig_ecc_peak_force.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    fig_ecc_peak_force.update_traces(marker_size=11)
    fig_ecc_peak_force.update_xaxes(rangebreaks=[dict(values=missingDates)])  #remove empty dates

    #Braking Duration graph
    braking_duration_name = df_selection.groupby(by=["Date"]).mean(numeric_only=True)[["Braking Phase Duration [s] "]]
    fig_braking_duration = px.line(
        braking_duration_name,
        braking_duration_name.index,
        y="Braking Phase Duration [s] ",
        title="<b>Braking Phase Duration</b>",
        color_discrete_sequence=["#3679ff"] * len(braking_duration_name),
        template="plotly_white",
        markers=True
    )
    #adding Average line
    fig_braking_duration.add_hline(y=braking_duration,line_dash="dash", line_color="black", annotation_text="Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="black")
    #adding team avg line
    fig_braking_duration.add_hline(y=braking_duration_team_avg,line_dash="dot", line_color="red", annotation_text="Team Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="red")

    fig_braking_duration.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    fig_braking_duration.update_traces(marker_size=11)
    fig_braking_duration.update_xaxes(rangebreaks=[dict(values=missingDates)]) #remove empty dates
    


    # TOP KPI's Performance
    peak_power = int(df_selection["Peak Power / BM [W/kg] "].mean())
    peak_power_team_avg = int(df_selection1["Peak Power / BM [W/kg] "].mean())
    jump_height = int(df_selection["Jump Height (Flight Time) in Inches [in] "].mean())
    jump_height_team_avg = int(df_selection1["Jump Height (Flight Time) in Inches [in] "].mean())
    RSI_mod = round(df_selection["RSI-modified [m/s] "].mean(),2)
    RSI_mod_team_avg = round(df_selection1["RSI-modified [m/s] "].mean(),2)
    conc_impulse =int(df_selection["Concentric Impulse [N s] "].mean())
    conc_impulse_team_avg =int(df_selection1["Concentric Impulse [N s] "].mean())
    ecc_impulse = int(df_selection["Eccentric Braking Impulse [N s] "].mean())
    ecc_impulse_team_avg = int(df_selection1["Eccentric Braking Impulse [N s] "].mean())

    #Most recent KPI's Performance
    jump_height_recent = int(df_selection[df_selection["Date"]==df_selection["Date"].max()]["Jump Height (Flight Time) in Inches [in] "].mean())
    peak_power_recent = int(df_selection[df_selection["Date"]==df_selection["Date"].max()]["Peak Power / BM [W/kg] "].mean())
    RSI_mod_recent = round(df_selection[df_selection["Date"]==df_selection["Date"].max()]["RSI-modified [m/s] "].mean(),2)
    conc_impulse_recent = int(df_selection[df_selection["Date"]==df_selection["Date"].max()]["Concentric Impulse [N s] "].mean())
    ecc_impulse_recent = int(df_selection[df_selection["Date"]==df_selection["Date"].max()]["Eccentric Braking Impulse [N s] "].mean())

    #calculations for percentages Performance
    jump_height_percentage = round(((jump_height_recent/jump_height)*100)-100)
    peak_power_percentage = round(((peak_power_recent/peak_power)*100)-100)
    RSI_mod_percentage = round(((RSI_mod_recent/RSI_mod)*100)-100)
    conc_impulse_percentage = round(((conc_impulse_recent/conc_impulse)*100)-100)
    ecc_impulse_percentage = round(((ecc_impulse_recent/ecc_impulse)*100)-100)

    #std
    jumpheight_std = int(df_selection["Jump Height (Flight Time) in Inches [in] "].std())
    peakpower_std = int(df_selection["Peak Power / BM [W/kg] "].std())
    RSImod_std = round(df_selection["RSI-modified [m/s] "].std(),2)
    concimp_std = int(df_selection["Concentric Impulse [N s] "].std())
    eccimp_std = int(df_selection["Eccentric Braking Impulse [N s] "].std())

    #benchmarks
    jumpheight_tscore = round(((((jump_height_recent - jump_height)/jumpheight_std)*10)+50))
    peakpower_tscore = round(((((peak_power_recent - peak_power)/peakpower_std)*10)+50))
    RSImod_tscore = round(((((RSI_mod_recent - RSI_mod)/RSImod_std)*10)+50))
    concimp_tscore = round(((((conc_impulse_recent - conc_impulse_recent)/concimp_std)*10)+50))
    eccimp_tscore = round(((((ecc_impulse_recent - ecc_impulse)/eccimp_std)*10)+50))
    
    #level 
    def level_jumpheight(jumpheight_tscore):
      if jumpheight_tscore >= 80:
        return str(jumpheight_tscore) + " - " + "Excellent"
      elif 70 < jumpheight_tscore < 80:
        return str(jumpheight_tscore) + " - " + "Very Good"
      elif 60 < jumpheight_tscore < 70:
        return str(jumpheight_tscore) + " - " + "Good"
      elif 55 < jumpheight_tscore < 60:
        return str(jumpheight_tscore) + " - " + "Above Avg"
      elif 45 < jumpheight_tscore < 55:
        return str(jumpheight_tscore) + " - " + "Average"
      elif 40 < jumpheight_tscore < 45:
        return str(jumpheight_tscore) + " - " + "Below Avg"
      elif 30 < jumpheight_tscore < 40:
        return str(jumpheight_tscore) + " - " + "Poor"
      elif 20 < jumpheight_tscore < 30:
        return str(jumpheight_tscore) + " - " + "Very Poor"
      elif jumpheight_tscore <= 20:
        return str(jumpheight_tscore) + " - " + "Extremely Poor"

    def level_peakpower(peakpower_tscore):
      if peakpower_tscore >= 80:
        return str(peakpower_tscore) + " - " + "Excellent"
      elif 70 < peakpower_tscore < 80:
        return str(peakpower_tscore) + " - " + "Very Good"
      elif 60 < peakpower_tscore < 70:
        return str(peakpower_tscore) + " - " + "Good"
      elif 55 < peakpower_tscore < 60:
        return str(peakpower_tscore) + " - " + "Above Avg"
      elif 45 < peakpower_tscore < 55:
        return str(peakpower_tscore) + " - " + "Average"
      elif 40 < peakpower_tscore < 45:
        return str(peakpower_tscore) + " - " + "Below Avg"
      elif 30 < peakpower_tscore < 40:
        return str(peakpower_tscore) + " - " + "Poor"
      elif 20 < peakpower_tscore < 30:
        return str(peakpower_tscore) + " - " + "Very Poor"
      elif peakpower_tscore <= 20:
        return str(peakpower_tscore) + " - " + "Extremely Poor"
 
    def level_RSImod(RSImod_tscore):
      if RSImod_tscore >= 80:
        return str(RSImod_tscore) + " - " + "Excellent"
      elif 70 < RSImod_tscore < 80:
        return str(RSImod_tscore) + " - " + "Very Good"
      elif 60 < RSImod_tscore < 70:
        return str(RSImod_tscore) + " - " + "Good"
      elif 55 < RSImod_tscore < 60:
        return str(RSImod_tscore) + " - " + "Above Avg"
      elif 45 < RSImod_tscore < 55:
        return str(RSImod_tscore) + " - " + "Average"
      elif 40 < RSImod_tscore < 45:
        return str(RSImod_tscore) + " - " + "Below Avg"
      elif 30 < RSImod_tscore < 40:
        return str(RSImod_tscore) + " - " + "Poor"
      elif 20 < RSImod_tscore < 30:
        return str(RSImod_tscore) + " - " + "Very Poor"
      elif RSImod_tscore <= 20:
        return str(RSImod_tscore) + " - " + "Extremely Poor"
      
    def level_concimp(concimp_tscore):
      if concimp_tscore >= 80:
        return str(concimp_tscore) + " - " + "Excellent"
      elif 70 < concimp_tscore < 80:
        return str(concimp_tscore) + " - " + "Very Good"
      elif 60 < concimp_tscore < 70:
        return str(concimp_tscore) + " - " + "Good"
      elif 55 < concimp_tscore < 60:
        return str(concimp_tscore) + " - " + "Above Avg"
      elif 45 < concimp_tscore < 55:
        return str(concimp_tscore) + " - " + "Average"
      elif 40 < concimp_tscore < 45:
        return str(concimp_tscore) + " - " + "Below Avg"
      elif 30 < concimp_tscore < 40:
        return str(concimp_tscore) + " - " + "Poor"
      elif 20 < concimp_tscore < 30:
        return str(concimp_tscore) + " - " + "Very Poor"
      elif concimp_tscore <= 20:
        return str(concimp_tscore) + " - " + "Extremely Poor"

    def level_eccimp(eccimp_tscore):
      if eccimp_tscore >= 80:
        return str(eccimp_tscore) + " - " + "Excellent"
      elif 70 < eccimp_tscore < 80:
        return str(eccimp_tscore) + " - " + "Very Good"
      elif 60 < eccimp_tscore < 70:
        return str(eccimp_tscore) + " - " + "Good"
      elif 55 < eccimp_tscore < 60:
        return str(eccimp_tscore) + " - " + "Above Avg"
      elif 45 < eccimp_tscore < 55:
        return str(eccimp_tscore) + " - " + "Average"
      elif 40 < eccimp_tscore < 45:
        return str(eccimp_tscore) + " - " + "Below Avg"
      elif 30 < eccimp_tscore < 40:
        return str(eccimp_tscore) + " - " + "Poor"
      elif 20 < eccimp_tscore < 30:
        return str(eccimp_tscore) + " - " + "Very Poor"
      elif eccimp_tscore <= 20:
        return str(eccimp_tscore) + " - " + "Extremely Poor"
        

    #functions for emojis Performance

    def jump_height_emoji(jump_height_percentage): 
      if jump_height_percentage < -5:
        return str(jump_height_percentage) + " % " + ":exclamation:"
      elif jump_height_percentage >5:
        return str(jump_height_percentage) + " % " + ":fire:"
      else:
        return str(jump_height_percentage) + " % " + ":thumbsup:"

    def peak_power_emoji(peak_power_percentage): 
      if peak_power_percentage < -5:
        return str(peak_power_percentage) + " % " + ":exclamation:"
      elif peak_power_percentage >5:
        return str(peak_power_percentage) + " % " + ":fire:"
      else:
        return str(peak_power_percentage) + " % " + ":thumbsup:"

    def RSI_mod_emoji(RSI_mod_percentage): 
      if RSI_mod_percentage < -5:
        return str(RSI_mod_percentage) + " % " + ":exclamation:"
      elif RSI_mod_percentage >5:
        return str(RSI_mod_percentage) + " % " + ":fire:"
      else:
        return str(cmj_depth_percentage) + " % " + ":thumbsup:"

    def conc_impulse_emoji(conc_impulse_percentage): 
      if conc_impulse_percentage < -5:
        return str(conc_impulse_percentage) + " % " + ":exclamation:"
      elif conc_impulse_percentage >5:
        return str(conc_impulse_percentage) + " % " + ":fire:"
      else:
        return str(conc_impulse_percentage) + " % " + ":thumbsup:"

    def ecc_impulse_emoji(ecc_impulse_percentage): 
      if ecc_impulse_percentage < -5:
        return str(ecc_impulse_percentage) + " % " + ":exclamation:"
      elif ecc_impulse_percentage >5:
        return str(ecc_impulse_percentage) + " % " + ":fire:"
      else:
        return str(ecc_impulse_percentage) + " % " + ":thumbsup:"



    #Graphs Performance KPI's


    jump_height_by_name = df_selection.groupby(by=["Date"]).mean()[["Jump Height (Flight Time) in Inches [in] "]]
    fig_jump_height = px.line(
        jump_height_by_name,
        x=jump_height_by_name.index,
        y="Jump Height (Flight Time) in Inches [in] ",
        title="<b>Jump Height</b>",
        color_discrete_sequence=["#3679ff"] * len(jump_height_by_name),
        template="plotly_white",
        markers=True
    )
    #adding Average line
    fig_jump_height.add_hline(y=jump_height,line_dash="dash", line_color="black", annotation_text="Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="black")
    #adding team Average line
    fig_jump_height.add_hline(y=jump_height_team_avg,line_dash="dot", line_color="red", annotation_text="Team Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="red")

    fig_jump_height.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    fig_jump_height.update_traces(marker_size=11)
    fig_jump_height.update_xaxes(rangebreaks=[dict(values=missingDates)]) #remove empty dates

    peak_power_by_name = df_selection.groupby(by=["Date"]).mean()[["Peak Power / BM [W/kg] "]]
    fig_peak_power = px.line(
        peak_power_by_name,
        x=peak_power_by_name.index,
        y="Peak Power / BM [W/kg] ",
        title="<b>Peak Power / BM</b>",
        color_discrete_sequence=["#3679ff"] * len(peak_power_by_name),
        template="plotly_white",
        markers=True
    )
    #adding Average line
    fig_peak_power.add_hline(y=peak_power,line_dash="dash", line_color="black", annotation_text="Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="black")
    #adding team Average line
    fig_peak_power.add_hline(y=peak_power_team_avg,line_dash="dot", line_color="red", annotation_text="Team Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="red")
    
    fig_peak_power.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    fig_peak_power.update_traces(marker_size=11)
    fig_peak_power.update_xaxes(rangebreaks=[dict(values=missingDates)]) #remove empty dates

    RSI_mod_by_name = df_selection.groupby(by=["Date"]).mean()[["RSI-modified [m/s] "]]
    fig_RSI_mod = px.line(
        RSI_mod_by_name,
        x=RSI_mod_by_name.index,
        y="RSI-modified [m/s] ",
        title="<b>RSI-modified</b>",
        color_discrete_sequence=["#3679ff"] * len(RSI_mod_by_name),
        template="plotly_white",
        markers=True
    )
    #adding Average line
    fig_RSI_mod.add_hline(y=RSI_mod,line_dash="dash", line_color="black", annotation_text="Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="black")
    #adding team Average line
    fig_RSI_mod.add_hline(y=RSI_mod_team_avg,line_dash="dot", line_color="red", annotation_text="Team Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="red")

    fig_RSI_mod.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    fig_RSI_mod.update_traces(marker_size=11)
    fig_RSI_mod.update_xaxes(rangebreaks=[dict(values=missingDates)]) #remove empty dates

    conc_impulse_by_name = df_selection.groupby(by=["Date"]).mean()[["Concentric Impulse [N s] "]]
    fig_conc_impulse = px.line(
        conc_impulse_by_name,
        x=conc_impulse_by_name.index,
        y="Concentric Impulse [N s] ",
        title="<b>Concentric Impulse</b>",
        color_discrete_sequence=["#3679ff"] * len(conc_impulse_by_name),
        template="plotly_white",
        markers=True
    )
    #adding Average line
    fig_conc_impulse.add_hline(y=conc_impulse,line_dash="dash", line_color="black", annotation_text="Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="black")
    #adding team Average line
    fig_conc_impulse.add_hline(y=conc_impulse_team_avg,line_dash="dot", line_color="red", annotation_text="Team Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="red")

    fig_conc_impulse.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    fig_conc_impulse.update_traces(marker_size=11)
    fig_conc_impulse.update_xaxes(rangebreaks=[dict(values=missingDates)]) #remove empty dates

    ecc_impulse_by_name = df_selection.groupby(by=["Date"]).mean()[["Eccentric Braking Impulse [N s] "]]
    fig_ecc_impulse = px.line(
        ecc_impulse_by_name,
        x=ecc_impulse_by_name.index,
        y="Eccentric Braking Impulse [N s] ",
        title="<b>Eccentric Braking Impulse</b>",
        color_discrete_sequence=["#3679ff"] * len(ecc_impulse_by_name),
        template="plotly_white",
        markers=True
    )
    #adding Average line
    fig_ecc_impulse.add_hline(y=ecc_impulse,line_dash="dash", line_color="black", annotation_text="Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="black")
    #adding Average line
    fig_ecc_impulse.add_hline(y=ecc_impulse_team_avg,line_dash="dot", line_color="red", annotation_text="Team Average", 
              annotation_position="bottom right",
              annotation_font_size=10,
              annotation_font_color="red")
              
    fig_ecc_impulse.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    fig_ecc_impulse.update_traces(marker_size=11)
    fig_ecc_impulse.update_xaxes(rangebreaks=[dict(values=missingDates)]) #remove empty dates


#Header Readiness
    def readiness():
        
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
        st.markdown("<h1 style='text-align: center; color: #00000;'>Readiness</h1>", unsafe_allow_html=True)
        st.markdown("#####")

    #Readiness KPI Columns   

        left_column, middle_column, right_column, far_right_column = st.columns(4)
        with left_column:
            st.subheader("Ecc Duration")
            st.markdown("###")
            st.markdown("##### Average:")
            st.write(f" {eccentric_duration:,}")
            st.markdown("##### Most Recent:")
            st.write(f" {ecc_duration_recent:,}")
            st.markdown("##### % Difference:")
            st.write(ecc_emoji(ecc_duration_percentage))
        with middle_column:
            st.markdown("### Ecc Peak Vel")
            st.markdown("###")
            st.markdown("##### Average:")
            st.write(f" {ecc_peak_velocity:,}")
            st.markdown("##### Most Recent:")
            st.write(f" {ecc_peak_vel_recent:,}")
            st.markdown("##### % Difference:")
            st.write(ecc_peak_vel_emoji(ecc_peak_vel_percentage))
        with right_column:
            st.markdown("### CMJ Depth")
            st.markdown("###")
            st.markdown("##### Average:")
            st.write(f" {cmj_depth:,}")
            st.markdown("##### Most Recent:")
            st.write(f" {cmj_depth_recent:,}")
            st.markdown("##### % Difference:")
            st.write(cmj_depth_emoji(cmj_depth_percentage))
        with far_right_column:
            st.markdown("### Ecc Decl RDF")
            st.markdown("###")
            st.markdown("##### Average:")
            st.write(f" {ecc_decl_rfd:,}")
            st.markdown("##### Most Recent:")
            st.write(f" {ecc_decl_rfd_recent:,}")
            st.markdown("##### % Difference:")
            st.write(ecc_decl_rfd_emoji(ecc_decl_rfd_percentage))
        
        left_column1, middle_column1, right_column1 = st.columns(3)
        with left_column1:
            st.subheader("Ecc Decl Impulse")
            st.markdown("###")
            st.markdown("##### Average:")
            st.write(f" {ecc_decl_imp:,}")
            st.markdown("##### Most Recent:")
            st.write(f" {ecc_decl_imp_recent:,}")
            st.markdown("##### % Difference:")
            st.write(ecc_decl_imp_emoji(ecc_decl_imp_percentage))
        with middle_column1:
            st.markdown("### Ecc Peak Force")
            st.markdown("###")
            st.markdown("##### Average:")
            st.write(f" {ecc_peak_force:,}")
            st.markdown("##### Most Recent:")
            st.write(f" {ecc_peak_force_recent:,}")
            st.markdown("##### % Difference:")
            st.write(ecc_peak_force_emoji(ecc_peak_force_percentage))
        with right_column1:
            st.markdown("### Braking Duration")
            st.markdown("###")
            st.markdown("##### Average:")
            st.write(f" {braking_duration:,}")
            st.markdown("##### Most Recent:")
            st.write(f" {braking_duration_recent:,}")
            st.markdown("##### % Difference:")
            st.write(braking_duration_emoji(braking_duration_percentage))
        st.markdown("""---""")
        
        st.plotly_chart(fig_ecc_duration, use_container_width=True)
        st.plotly_chart(fig_ecc_peak_vel, use_container_width=True)
        st.plotly_chart(fig_cmj_depth, use_container_width=True)
        st.plotly_chart(fig_ecc_decl_rfd, use_container_width=True)
        st.plotly_chart(fig_ecc_decl_imp, use_container_width=True)
        st.plotly_chart(fig_ecc_peak_force, use_container_width=True)
        st.plotly_chart(fig_braking_duration, use_container_width=True)
          
      
        st.caption(":thumbsup: = between -5 to 5% diff")
        st.caption(":fire: = more than 5% improvement")
        st.caption(":exclamation: = more than 5% decline")

    def performance():

        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
        st.markdown("<h1 style='text-align: center; color: #00000;'>Performance</h1>", unsafe_allow_html=True)
        st.markdown("#####")
        
        #performance KPI's
        
        
        left_column2, middle_left_column2, middle_column2 = st.columns(3)
        with left_column2:
            st.markdown("#### Jump Height")
            st.markdown("####")
            st.markdown("##### Average:")
            st.write(f" {jump_height:,}")
            st.markdown("##### Most Recent:")
            st.write(f" {jump_height_recent:,}")
            st.markdown("##### % Difference:")
            st.write(jump_height_emoji(jump_height_percentage))
        with middle_left_column2:
            st.markdown("#### Peak Power/BM")
            st.markdown("####")
            st.markdown("##### Average:")
            st.write(f" {peak_power:,}")
            st.markdown("##### Most Recent:")
            st.write(f" {peak_power_recent:,}")
            st.markdown("##### % Difference:")
            st.write(peak_power_emoji(peak_power_percentage))
        with middle_column2:
            st.markdown("#### RSI Mod")
            st.markdown("####")
            st.markdown("##### Average:")
            st.write(f" {RSI_mod:,}")
            st.markdown("##### Most Recent:")
            st.write(f" {RSI_mod_recent:,}")
            st.markdown("##### % Difference:")
            st.write(RSI_mod_emoji(cmj_depth_percentage))
        
        middle_right_column2,right_column2= st.columns(2)
        with middle_right_column2:
            st.markdown("### Concentric Impulse")
            st.markdown("####")
            st.markdown("##### Average:")
            st.write(f" {conc_impulse:,}")
            st.markdown("##### Most Recent:")
            st.write(f" {conc_impulse_recent:,}")
            st.markdown("##### % Difference:")
            st.write(conc_impulse_emoji(conc_impulse_percentage))
        with right_column2:
            st.markdown("### Eccentric Impulse")
            st.markdown("####")
            st.markdown("##### Average:")
            st.write(f" {ecc_impulse:,}")
            st.markdown("##### Most Recent:")
            st.write(f" {ecc_impulse_recent:,}")
            st.markdown("##### % Difference:")
            st.write(ecc_impulse_emoji(ecc_impulse_percentage))

        st.markdown("""---""")

        st.plotly_chart(fig_jump_height, use_container_width=True)
        st.plotly_chart(fig_peak_power, use_container_width=True)
        st.plotly_chart(fig_RSI_mod, use_container_width=True)
        st.plotly_chart(fig_conc_impulse, use_container_width=True)
        st.plotly_chart(fig_ecc_impulse, use_container_width=True)

        st.caption(":thumbsup: = between -5 to 5% diff")
        st.caption(":fire: = more than 5% improvement")
        st.caption(":exclamation: = more than 5% decrease")

    def interactive_graphs():
        
        st.markdown("<h1 style='text-align: center; color: #00000;'>Interactice Graphs</h1>", unsafe_allow_html=True)
        st.markdown("#####")
        st.subheader("Compare data between athletes")
        st.write("Select the athletes that you want to compare in the navigation bar")
        st.markdown('###')

        df_nonameordate = df_selection.drop(['Date','Name'], axis=1)
        dfdateorname=df_selection.drop(['Peak Power / BM [W/kg] ','RSI-modified [m/s] ','Concentric Impulse [N s] ','Eccentric Braking Impulse [N s] ',
                                  'Eccentric Duration [ms] ','Countermovement Depth [cm] ','Eccentric Peak Velocity [m/s] ',
                                  'Takeoff Peak Force [N] (Asym) (%)','Peak Landing Force [N] (Asym) (%)',
                                  'Eccentric Braking Impulse [N s] (Asym) (%)','Eccentric Deceleration RFD [N/s] (Asym) (%)',
                                  'Jump Height (Flight Time) in Inches [in] ',"Eccentric Deceleration RFD [N/s] ", "Eccentric Deceleration Impulse [N s] ",
                                  "Eccentric Peak Force [N] ","Braking Phase Duration [s] "], axis=1)
        
        col1,col2 = st.columns(2)
        y_axis_val = col1.selectbox('Select the Metric', options=df_nonameordate.columns)

        plot = px.line(df_selection, x=df_selection['Date'], y=y_axis_val, color=df_selection['Name'], text=y_axis_val)
        plot.update_layout(
        xaxis=dict(tickmode="linear"),
        )
        plot.update_xaxes(rangebreaks=[dict(values=missingDates)]) #remove empty dates
        plot.update_traces(marker_size=11, textposition='top center')
        st.plotly_chart(plot, use_container_width=True)
        
        st.markdown("""---""")
        st.subheader('Comparasion between two metrics')
        st.write("Select only a few athletes in the navigation bar for best visual")
        st.markdown('###')

        
        df_perfandread = df_nonameordate.drop(['Takeoff Peak Force [N] (Asym) (%)','Peak Landing Force [N] (Asym) (%)',
                                  'Eccentric Braking Impulse [N s] (Asym) (%)','Eccentric Deceleration RFD [N/s] (Asym) (%)'], axis=1)
        sb_options = list(df_perfandread.columns)

        colselect1, colselect2 = st.columns(2)
        with colselect1:
          select1 = st.selectbox('Select the X-axis', options=sb_options)
        with colselect2:     
          select2 = st.selectbox('Select the Y-axis', options=sb_options, index=1)
        
        #scatter plot
        plot3 = px.scatter(df_selection, x=select1, y=select2, title= select2 + ' VS ' + select1, text='Date', color='Name')
        plot3.update_traces(marker_size=11, textposition='top center')

        st.plotly_chart(plot3, use_container_width=True)

    def assym():
        st.markdown("<h1 style='text-align: center; color: #00000;'>Asymmetries</h1>", unsafe_allow_html=True)
        st.markdown("#####")
        st.write("Select only 1 athlete in the navigation bar for best visual")
        st.markdown('###')

        dfdateorname=df_selection.drop(['Peak Power / BM [W/kg] ','RSI-modified [m/s] ','Concentric Impulse [N s] ','Eccentric Braking Impulse [N s] ',
                                  'Eccentric Duration [ms] ','Countermovement Depth [cm] ','Eccentric Peak Velocity [m/s] ',
                                  'Takeoff Peak Force [N] (Asym) (%)','Peak Landing Force [N] (Asym) (%)',
                                  'Eccentric Braking Impulse [N s] (Asym) (%)','Eccentric Deceleration RFD [N/s] (Asym) (%)',
                                  'Jump Height (Flight Time) in Inches [in] ',"Eccentric Deceleration RFD [N/s] ", "Eccentric Deceleration Impulse [N s] ",
                                  "Eccentric Peak Force [N] ","Braking Phase Duration [s] "], axis=1)

        #Take off PeakForce
        fd = df_selection['Takeoff Peak Force [N] (Asym) (%)']
        TakeoffPeakForce = [float(each.upper().replace('R','').strip()) if 'R' in each.upper() else -float(each.upper().replace('L','').strip()) for each in fd]
        
        #Peak Landing Force
        fd1 = df_selection['Peak Landing Force [N] (Asym) (%)']
        PeakLandingForce = [float(each.upper().replace('R','').strip()) if 'R' in each.upper() else -float(each.upper().replace('L','').strip()) for each in fd1]

        #Peak Landing Force
        fd2 = df_selection['Eccentric Braking Impulse [N s] (Asym) (%)']
        EccentricBrakingImpulse = [float(each.upper().replace('R','').strip()) if 'R' in each.upper() else -float(each.upper().replace('L','').strip()) for each in fd2]

        #Peak Landing Force
        fd3 = df_selection['Eccentric Deceleration RFD [N/s] (Asym) (%)']
        EccentricDeclRFD = [float(each.upper().replace('R','').strip()) if 'R' in each.upper() else -float(each.upper().replace('L','').strip()) for each in fd3]
        
        
        dateorname,get_list = st.columns(2)
        with dateorname:
          dateorname =st.selectbox('Select the X-axis', options=dfdateorname.columns, index=1)
        with get_list:
          get_list = st.selectbox('Select Asymmetry', ("TakeoffPeakForce",'PeakLandingForce','EccentricBrakingImpulse','EccentricDeclRFD'))
        if get_list == "TakeoffPeakForce":
          select_options = TakeoffPeakForce
        elif get_list == "PeakLandingForce":
          select_options = PeakLandingForce
        elif get_list == "EccentricBrakingImpulse":
          select_options = EccentricBrakingImpulse
        elif get_list == "EccentricDeclRFD":
          select_options = EccentricDeclRFD

        plot_assym = px.bar(df_selection, x=select_options, y=dateorname, text=select_options, color=dateorname,
                            labels={
                            "X": "Asymmetry",
                            },template="plotly_white")
        plot_assym.update_yaxes(rangebreaks=[dict(values=missingDates)]) #remove empty dates
        plot_assym.update_traces(textposition='outside', textfont_size=18)
        
        st.plotly_chart(plot_assym, use_container_width=True)

       

        st.caption('Negative Values = Left Asymmetry')
        st.caption('Postive Values = Right Asymmetry')
        
        st.markdown('#')
        st.subheader('Data Table Asymmetry')
        df_asym=df_selection.drop(['Peak Power / BM [W/kg] ','RSI-modified [m/s] ','Concentric Impulse [N s] ','Eccentric Braking Impulse [N s] ',
                                  'Eccentric Duration [ms] ','Countermovement Depth [cm] ','Eccentric Peak Velocity [m/s] ',
                                  'Jump Height (Flight Time) in Inches [in] ',"Eccentric Deceleration RFD [N/s] ", "Eccentric Deceleration Impulse [N s] ",
                                  "Eccentric Peak Force [N] ","Braking Phase Duration [s] "], axis=1)
        st._legacy_dataframe(df_asym)

    #leaderboard
    def leaderboard():
      st.markdown("<h1 style='text-align: center; color: #00000;'>Leaderboard</h1>", unsafe_allow_html=True)
      st.markdown("#####")

      df_perfandread = df_selection.drop(['Takeoff Peak Force [N] (Asym) (%)','Peak Landing Force [N] (Asym) (%)',
                                  'Eccentric Braking Impulse [N s] (Asym) (%)','Eccentric Deceleration RFD [N/s] (Asym) (%)','Date'], axis=1)

      sb_options = list(df_perfandread.columns)
      sb_options.remove('Name')

      st.write("For best visual select only one date")

      colselect1,colselect2 = st.columns(2)
      with colselect1:
        sel_metric = st.selectbox('Select the Metric', options=sb_options)
      with colselect2:
        st.write("")

      # Create a new dataframe for plotting. Sort it for plotting display.
      # If metric value is the same, display name by alphabetic order.
      df_metric = df_perfandread.copy()
      df_metric = df_metric.sort_values(by=[sel_metric,'Name'], ascending=[True, False])
      
      plot_leaderboard = px.bar(df_metric, x=sel_metric, y="Name", template="plotly_white", color=sel_metric, text_auto=True)
      plot_leaderboard.update_layout(paper_bgcolor = "rgba(0,0,0,0)",
                  plot_bgcolor = "rgba(0,0,0,0)")
      st.plotly_chart(plot_leaderboard, use_container_width=True)

    def benchmarks():
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

        st.markdown("<h1 style='text-align: center; color: #00000;'>T-Score Benchmarks</h1>", unsafe_allow_html=True)
        st.markdown("#####")

        col1,col2,col3,col4,col5, = st.columns(5)
        with col1:
          st.markdown("###### Jump Height")
          st.markdown("#####")
          st.write(level_jumpheight(jumpheight_tscore))
        with col2:
          st.markdown("###### Peak Power")
          st.markdown("#####")
          st.write(level_peakpower(peakpower_tscore))
        with col3:
          st.markdown("###### RSI Mod")
          st.markdown("#####")
          st.write(level_RSImod(RSImod_tscore))
        with col4:
          st.markdown("###### Concentric Impulse")
          st.markdown("#####")
          st.write(level_concimp(concimp_tscore))
        with col5:
          st.markdown("###### Eccentric Impulse")
          st.markdown("#####")
          st.write(level_eccimp(eccimp_tscore))

        st.write("Excellent >= 80")
        st.write("Very Good 70-80")
        st.write("Good 60-70")
        st.write("Above Average 55-60")
        st.write("Average 45-55")
        st.write("Below Average 40-45")
        st.write("Poor 30-40")
        st.write("Very Poor 20-30")
        st.write("Extremely Poor <=20")

    def all_data():
        st.header('All Data')
        st.markdown("#")
        
        st._legacy_dataframe(df_selection)


    if options == 'Readiness':
        readiness()
    elif options == 'Performance':
        performance()
    elif options == 'Interactive Graphs':
        interactive_graphs()  
    elif options == 'Assymetries':
        assym()
    elif options == 'Leaderboard':
        leaderboard()
    elif options == 'Benchmarks':
        benchmarks()
    elif options == 'All Data':
        all_data()

  else:
    st.warning('Incorrect Password')

