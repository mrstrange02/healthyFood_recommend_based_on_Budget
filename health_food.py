{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 26,
   "id": "52e18851-49b5-46a2-8c5c-ce1af703b6d0",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import streamlit as st\n",
    "\n",
    "# Load dataset\n",
    "df = pd.read_csv('healthy_foods_dataset_final.csv')\n",
    "\n",
    "def recommend_foods(budget, categories, top_n=3):\n",
    "    # Filter selected categories\n",
    "    filtered = df[df['Category'].isin(categories)].copy()\n",
    "    # Nutrition score: (protein + fiber)/ price\n",
    "    filtered['nutrient_score'] = (filtered['Protein (g)'] + filtered['Fiber (g)']) / filtered['Price (₹/kg)']\n",
    "    filtered = filtered.sort_values(by='nutrient_score', ascending=False)\n",
    "    \n",
    "    recommendations = []\n",
    "    for _ in range(top_n):\n",
    "        selected = []\n",
    "        total_cost = 0\n",
    "        for _, row in filtered.iterrows():\n",
    "            if total_cost + row['Price (₹/kg)'] <= budget:\n",
    "                selected.append(f\"{row['Food Item']} (₹{row['Price (₹/kg)']})\")\n",
    "                total_cost += row['Price (₹/kg)']\n",
    "        recommendations.append(selected)\n",
    "    \n",
    "    return recommendations\n",
    "\n",
    "# Streamlit UI\n",
    "st.title('Healthy Food Recommendation Based on Budget')\n",
    "\n",
    "budget = st.number_input('Enter your budget (₹)', min_value=1)\n",
    "categories = st.multiselect('Select Food Categories', options=df['Category'].unique())\n",
    "\n",
    "if st.button('Get Recommendations'):\n",
    "    if not categories:\n",
    "        st.warning('Please select at least one food category.')\n",
    "    else:\n",
    "        recs = recommend_foods(budget, categories)\n",
    "        for i, rec in enumerate(recs, 1):\n",
    "            st.subheader(f'Set {i}')\n",
    "            if rec:\n",
    "                for item in rec:\n",
    "                    st.write(item)\n",
    "            else:\n",
    "                st.write('No foods found within budget.')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8613c10e-41ae-466f-9987-f54a18bc2f48",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b534d51d-fa5b-4fbe-9c37-516dd4788898",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
