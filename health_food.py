import pandas as pd
import streamlit as st

# Load updated dataset
df = pd.read_csv('healthy_foods_dataset_final_updated.csv')

def recommend_foods_varied(budget, categories, use_half_price=True, top_n=3):
    filtered = df[df['Category'].isin(categories)].copy()
    price_column = 'Half Price (₹/kg)' if use_half_price else 'Price (₹/kg)'
    filtered['nutrient_score'] = (filtered['Protein (g)'] + filtered['Fiber (g)']) / filtered[price_column]
    filtered = filtered.sort_values(by='nutrient_score', ascending=False)

    recommendations = []
    remaining = filtered.copy()

    for _ in range(top_n):
        selected = []
        total_cost = 0
        total_protein = 0
        total_fiber = 0

        for idx, row in remaining.iterrows():
            if total_cost + row[price_column] <= budget:
                selected.append(row)
                total_cost += row[price_column]
                total_protein += row['Protein (g)']
                total_fiber += row['Fiber (g)']

        recommendations.append({
            'items': selected,
            'total_cost': total_cost,
            'total_protein': total_protein,
            'total_fiber': total_fiber
        })

        selected_items = [item['Food Item'] for item in selected]
        remaining = remaining[~remaining['Food Item'].isin(selected_items)]

        if remaining.empty:
            break

    return recommendations

# Streamlit UI
st.title('Healthy Food Recommendation Based on Budget')

st.markdown("""
Welcome! This app helps you choose the best healthy foods within your given budget. 
Select your preferred food categories and enter your budget to see multiple nutritious sets tailored for you.
""")

budget = st.number_input('Enter your budget (₹)', min_value=1)
categories = st.multiselect('Select Food Categories', options=df['Category'].unique())
use_half_price = st.checkbox('Use Half Price for calculations', value=True)

if st.button('Get Recommendations'):
    if not categories:
        st.warning('Please select at least one food category.')
    else:
        recs = recommend_foods_varied(budget, categories, use_half_price)
        for i, rec in enumerate(recs, 1):
            st.subheader(f'Set {i}')
            if rec['items']:
                st.write(f"**Total Cost:** ₹{rec['total_cost']:.2f}")
                st.write(f"**Total Protein:** {rec['total_protein']:.2f} g")
                st.write(f"**Total Fiber:** {rec['total_fiber']:.2f} g")
                st.markdown("**Recommended Foods:**")
                for item in rec['items']:
                    st.markdown(f"- {item['Food Item']} (₹{item['Price (₹/kg)']:.1f}, Protein: {item['Protein (g)']} g, Fiber: {item['Fiber (g)']} g)")
            else:
                st.write('No foods found within budget.')
