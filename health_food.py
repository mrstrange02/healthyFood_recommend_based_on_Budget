import pandas as pd
import streamlit as st

# Load updated dataset
df = pd.read_csv('healthy_foods_dataset_final2.csv')

def recommend_foods_varied(budget, categories, use_half_price=True, top_n=3):
    filtered = df[df['Category'].isin(categories)].copy()
    price_column = 'Half Price (₹/kg)' if use_half_price else 'Price (₹/kg)'
    filtered['nutrient_score'] = (filtered['Protein (g)'] + filtered['Fiber (g)']) / filtered[price_column]
    filtered = filtered.sort_values(by='nutrient_score', ascending=False)

    recommendations = []
    remaining = filtered.copy()

    for _ in range(top_n):
        selected_rows = []
        total_cost = 0
        total_protein = 0
        total_fiber = 0

        for idx, row in remaining.iterrows():
            if total_cost + row[price_column] <= budget:
                selected_rows.append(row)
                total_cost += row[price_column]
                total_protein += row['Protein (g)']
                total_fiber += row['Fiber (g)']

        recommended_df = pd.DataFrame(selected_rows)
        recommendations.append({
            'dataframe': recommended_df,
            'total_cost': total_cost,
            'total_protein': total_protein,
            'total_fiber': total_fiber
        })

        selected_items = recommended_df['Food Item'].tolist()
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

budget = st.number_input('Enter your budget (₹)', min_value=1, value=500)
categories = st.multiselect('Select Food Categories', options=df['Category'].unique())
use_half_price = st.checkbox('Use Half Price for calculations', value=True)

if st.button('Get Recommendations'):
    if not categories:
        st.warning('Please select at least one food category.')
    else:
        recs = recommend_foods_varied(budget, categories, use_half_price)
        for i, rec in enumerate(recs, 1):
            st.subheader(f'Set {i}')
            if not rec['dataframe'].empty:
                # Display summary with metric widgets
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Cost (₹)", f"{rec['total_cost']:.2f}")
                col2.metric("Total Protein (g)", f"{rec['total_protein']:.2f}")
                col3.metric("Total Fiber (g)", f"{rec['total_fiber']:.2f}")

                # Show recommended foods in a table
                st.dataframe(rec['dataframe'][['Food Item', 'Category', 'Price (₹/kg)', 'Protein (g)', 'Fiber (g)', 'Calories']].style.format({
                    'Price (₹/kg)': '₹{:.2f}',
                    'Protein (g)': '{:.2f}',
                    'Fiber (g)': '{:.2f}',
                    'Calories': '{:.0f}'
                }))
            else:
                st.info('No foods found within budget.')
