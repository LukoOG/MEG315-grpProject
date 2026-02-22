import streamlit as st
from cycle.ad_model import analyze_ad
from cycle.htc_model import analyze_htc
from cycle.gas_cycle import brayton_cycle
from cycle.steam_cycle import rankine_cycle
from plots.diagrams import plot_ts, plot_hs
import matplotlib.pyplot as plt

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import pagesizes
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io
from datetime import datetime

def generate_pdf_report(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=pagesizes.A4)
    elements = []

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    normal_style = styles["Normal"]

    # Title
    elements.append(Paragraph("AD-HTC Enhanced Combined Cycle Report", title_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Timestamp
    elements.append(Paragraph(
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        normal_style
    ))
    elements.append(Spacer(1, 0.3 * inch))

    # Table Data
    table_data = [
        ["Parameter", "Value"],
        ["Brayton Efficiency (%)", f"{data['brayton_eff']:.2f}"],
        ["Rankine Efficiency (%)", f"{data['rankine_eff']:.2f}"],
        ["Overall Efficiency (%)", f"{data['overall_eff']:.2f}"],
        ["Air Mass Flow (kg/s)", f"{data['m_air']:.2f}"],
        ["Steam Mass Flow (kg/s)", f"{data['m_steam']:.2f}"],
        ["Total Power Output (kW)", f"{data['total_power']:.2f}"],
        ["Hydrochar Energy (kW)", f"{data['hydrochar_energy']:.2f}"],
    ]

    table = Table(table_data, colWidths=[3 * inch, 2 * inch])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer

def main():
    st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight:600;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="big-font">Combined Cycle Power Plant Results</p>', unsafe_allow_html=True)

    st.set_page_config(layout="wide")
    st.title("AD-HTC Fuel Enhanced Combined Cycle Simulator")

    tab1, tab2, tab3 = st.tabs([
        "Analysis",
        "Download Report",
        "Cycle Schematic"
    ])

    st.sidebar.header("AD Parameters")

    m_biomass = st.sidebar.number_input("Biomass flow (kg/s)", value=5.0)
    vs_fraction = st.sidebar.slider("Volatile Solids Fraction", 0.1, 1.0, 0.8)
    methane_yield = st.sidebar.number_input("Methane yield (m3/kg VS)", value=0.35)

    st.sidebar.header("HTC Parameters")

    char_yield = st.sidebar.slider("Hydrochar Yield Fraction", 0.3, 0.8, 0.6)
    htc_eff = st.sidebar.slider("HTC Energy Efficiency", 0.5, 1.0, 0.85)
    energy_density = st.sidebar.slider("Energy Density Factor", 1.0, 2.0, 1.5)

    st.sidebar.header("Brayton Parameters")

    T1 = st.sidebar.number_input("Compressor Inlet Temp (K)", value=300.0)
    P1 = st.sidebar.number_input("Compressor Inlet Pressure (kPa)", value=100.0)
    rp = st.sidebar.number_input("Pressure Ratio", value=8.0)
    T3 = st.sidebar.number_input("Turbine Inlet Temp (K)", value=1200.0)
    eta_c = st.sidebar.slider("Compressor Efficiency", 0.6, 1.0, 0.85)
    eta_t_gas = st.sidebar.slider("Gas Turbine Efficiency", 0.6, 1.0, 0.9)
    m_air = st.sidebar.number_input("Air Mass Flow (kg/s)", value=10.0)

    st.sidebar.header("Rankine Parameters")

    P_boiler = st.sidebar.number_input("Boiler Pressure (Pa)", value=8e6)
    T_superheat = st.sidebar.number_input("Superheat Temp (K)", value=773.0)
    P_cond = st.sidebar.number_input("Condenser Pressure (Pa)", value=10000.0)
    eta_t_steam = st.sidebar.slider("Steam Turbine Efficiency", 0.6, 1.0, 0.9)
    eta_p = st.sidebar.slider("Pump Efficiency", 0.6, 1.0, 0.85)
    m_steam = st.sidebar.number_input("Steam Mass Flow (kg/s)", value=5.0)

    # =========================
    # RUN ANALYSIS
        # =========================
    with tab1:
        if st.button("Run Integrated Analysis"):

            # --- AD ---
            ad = analyze_ad(m_biomass, vs_fraction, methane_yield)

            # --- HTC ---
            htc = analyze_htc(
                ad["digestate_mass"],
                char_yield,
                energy_density,
                htc_eff
            )

            # --- Fuel Energy ---
            fuel_energy = (
                ad["biogas_energy"] +
                htc["hydrochar_energy"]
            )

            brayton_results = brayton_cycle(
                T1, P1, rp, T3,
                eta_c, eta_t_gas,
                m_air
            )

            rankine_results = rankine_cycle(
                P_boiler, T_superheat, P_cond,
                eta_t_steam, eta_p,
                m_steam
            )

            # --- Power Calculation ---
            brayton_power = brayton_results["Net Work (kW)"]

            rankine_power = (
                rankine_results["Turbine Work (kW)"] -
                rankine_results["Pump Work (kW)"]
            )

            total_power = brayton_power + rankine_power

            overall_eff = total_power / fuel_energy

            # st.subheader("System Efficiencies")
            # st.write("Brayton Efficiency:", brayton_results["Brayton Efficiency"])
            # st.write("Rankine Efficiency:", rankine_results["Rankine Efficiency"])
            # st.write("Overall System Efficiency:", overall_eff)
            
            brayton_eff = brayton_results["Brayton Efficiency"] * 100
            rankine_eff = rankine_results["Rankine Efficiency"] * 100

            # st.metric("Brayton Efficiency (%)", f"{brayton_eff:.2f} %")
            # st.metric("Rankine Efficiency (%)", f"{rankine_eff:.2f} %")
            # st.metric("Overall System Efficiency (%)", f"{overall_eff:.2f} %")
            
            st.session_state.report_data = {
                "brayton_eff": brayton_eff,
                "rankine_eff": rankine_eff,
                "overall_eff": overall_eff * 100,
                "m_air": brayton_results["Mass Flow Air (kg/s)"],
                "m_steam": rankine_results["Mass Flow Steam (kg/s)"],
                "total_power": total_power,
                "hydrochar_energy": htc["hydrochar_energy"],
                "brayton_results": brayton_results,
                "rankine_results": rankine_results,
            }
            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader("Brayton Cycle")
                st.metric("Efficiency", f"{brayton_eff:.2f} %")
                st.metric("Mass Flow Air", f"{brayton_results['Mass Flow Air (kg/s)']:.2f} kg/s")
                st.metric("Net Work", f"{brayton_results['Net Work (kW)']:.2f} kW")

            with col2:
                st.subheader("Rankine Cycle")
                st.metric("Efficiency", f"{rankine_eff:.2f} %")
                st.metric("Mass Flow Steam", f"{rankine_results['Mass Flow Steam (kg/s)']:.2f} kg/s")
                st.metric("Net Work", f"{rankine_power:.2f} kW")

            with col3:
                st.subheader("Overall System")
                st.metric("Overall Efficiency", f"{overall_eff:.2f} %")
                st.metric("Total Power Output", f"{total_power:.2f} kW")

        st.subheader("Cycle Diagrams")

        if "report_data" in st.session_state:

            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)

            with col1:
                st.pyplot(plot_ts(st.session_state.report_data.get("brayton_results")))

            with col2:
                st.pyplot(plot_hs(st.session_state.report_data.get("rankine_results")))

        else:
            st.info("Run the Integrated Analysis to generate diagrams.")

    with tab2:   # or whichever tab is your download tab
        st.subheader("Download Structured PDF Report")

        if "report_data" in st.session_state:

            pdf_buffer = generate_pdf_report(st.session_state.report_data)

            st.download_button(
                label="Download PDF Report",
                data=pdf_buffer,
                file_name="AD_HTC_Combined_Cycle_Report.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("Run the Integrated Analysis before downloading the report.")
        
    with tab3:
        st.subheader("AD-HTC Combined Cycle Schematic")

        with open("schematic.html", "r", encoding="utf-8") as f:
            html_data = f.read()

        st.components.v1.html(html_data, height=700, scrolling=True)
        
if __name__ == "__main__":
    main()