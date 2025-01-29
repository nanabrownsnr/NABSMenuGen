import streamlit as st
import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

st.set_page_config(page_title=None, page_icon=None, layout="wide")

def create_menu_app():
    st.title("NABS Weekly Menu Generator")
    
    # Client selection
    clients = ["Ecobank", "West African Pipeline", "Cradle To Crayons Crèche", 
               "IT Consortium", "Joshob Construction"]
    selected_client = st.selectbox("Select Client:", clients)
    
    # Date selection
    week_start = st.date_input("Select Week Starting Date:", 
                              datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()))
    
    # Menu component options
    carbohydrate = ["N/A", "Jollof Rice", "Waakye", "Banku", "Fried Rice", "Fufu", "Rice Balls", "Yam"]
    protein = ["N/A", "Grilled Chicken", "Crispy Chicken", "Fried Fish", "Grilled Fish", "Grilled Tilapia", "Fried Tilapia", "Sardine", "Fried Egg", "Beef"]
    sauce = ["N/A", "Shito", "Green Pepper", "Red Pepper", "Plain Stew", "Beef Stew", "Okro Soup", "Light Soup", "Groundnut Soup", "Palm Nut Soup", "Tilapia Light Soup", "Garden Egg Stew", "Kontomire Stew"]
    extras = ["N/A", "Salad", "Boiled Egg", "Sausage", "Steamed Vegetables"]
    dessert = ["N/A", "Bananas", "Pineapples", "Oranges", "Ice Cream", "Sobolo"]
    
    # Create dictionary to store selections
    menu_selections = {}
    dessert_selections = {}
    
    # Weekdays
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    st.subheader("Select Menu Items")
    for day in days:
        col1, col2, col3, col4, col5= st.columns(5)
        with col1:
            selected_carbohydrate = st.selectbox(f"{day} - Carbohydrate:", carbohydrate)
        with col2:
            selected_protein = st.selectbox(f"{day} - Protein:", protein)
        with col3:    
            selected_sauce = st.selectbox(f"{day} - Sauce:", sauce)
        with col4:    
            selected_extras = st.selectbox(f"{day} - Extras:", extras)
        with col5:    
            selected_dessert = st.selectbox(f"{day} - Dessert:", dessert)
        
        meal_components = [ selected_carbohydrate, selected_protein, selected_sauce, selected_extras]
        meal = ', '.join([item for item in meal_components if item != "N/A"])
        menu_selections[day] = meal if meal else "N/A"
        dessert_selections[day] = selected_dessert if selected_dessert != "N/A" else "N/A"
        
        st.divider() 
    
    if st.button("Generate PDF"):
        pdf_buffer = generate_pdf(selected_client, week_start, menu_selections, dessert_selections)
        st.download_button(
            label="Download Menu PDF",
            data=pdf_buffer,
            file_name=f"menu_{selected_client}_{week_start}.pdf",
            mime="application/pdf"
        )

def generate_pdf(client, week_start, menu_selections, dessert_selections):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Logo
    logo_path = "Nabs Logo.jpg"
    elements.append(Image(logo_path, width=150, height=75))
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceBefore=5,
        spaceAfter=20,
        alignment=1  # Center alignment
    )
    
    # Title
    title = Paragraph(f"Weekly Menu - {client}", title_style)
    subtitle = Paragraph(f"Week Starting: {week_start.strftime('%B %d, %Y')}", styles['Normal'])
    elements.extend([title, subtitle, Spacer(5, 10)])
    
    # Create table data with a separate column for desserts
    data = [["Day", "Menu Item", "Dessert"]]
    for day, meal in menu_selections.items():
        dessert = dessert_selections.get(day, "N/A")
        data.append([day, meal, dessert])
    
    # Create table
    table = Table(data, colWidths=[80, 250, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    
    elements.append(table)
    
    # Footer
    elements.extend([
        Spacer(1, 20),
        Paragraph("Note: Menu is generated based on ingredient availability.", styles['Italic'])
    ])
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

if __name__ == "__main__":
    create_menu_app()
