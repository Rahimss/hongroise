import streamlit as st
import numpy as np

# Hungarian Algorithm Implementation
def hungarian_algorithm(cost_matrix):
    n, m = cost_matrix.shape
    assert n <= m, "Cost matrix must have more columns than rows"

    # Step 1: Subtract the minimum value of each row from the row
    cost_matrix = cost_matrix - cost_matrix.min(axis=1, keepdims=True)

    # Step 2: Subtract the minimum value of each column from the column
    cost_matrix = cost_matrix - cost_matrix.min(axis=0, keepdims=True)

    # Step 3: Cover all zeros with a minimum number of lines
    covered_rows = np.zeros(n, dtype=bool)
    covered_cols = np.zeros(m, dtype=bool)
    zero_locations = np.where(cost_matrix == 0)
    assignment = np.full(n, -1)

    for i, j in zip(*zero_locations):
        if not covered_rows[i] and not covered_cols[j]:
            assignment[i] = j
            covered_rows[i] = True
            covered_cols[j] = True

    # Step 4: If all rows are assigned, return the assignment
    if np.all(covered_rows):
        return assignment

    # Step 5: Otherwise, find the minimum uncovered value and adjust the cost matrix
    while not np.all(covered_rows):
        min_uncovered = np.min(cost_matrix[~covered_rows][:, ~covered_cols])
        cost_matrix[~covered_rows] -= min_uncovered
        cost_matrix[:, covered_cols] += min_uncovered

        # Repeat steps 3-5 until all rows are assigned
        zero_locations = np.where(cost_matrix == 0)
        for i, j in zip(*zero_locations):
            if not covered_rows[i] and not covered_cols[j]:
                assignment[i] = j
                covered_rows[i] = True
                covered_cols[j] = True

    return assignment

# Function to convert a rectangular matrix to a square matrix
def make_square(matrix):
    n, m = matrix.shape
    max_size = max(n, m)
    square_matrix = np.zeros((max_size, max_size))
    square_matrix[:n, :m] = matrix
    return square_matrix

# Streamlit App
def main():
    st.title("algorithme hongrois BY DEBIECHE")
    

    # Input matrix dimensions
    st.write("Enter the dimensions of the cost matrix:")
    n = st.number_input("Numbre lignes (n)", min_value=1, value=3, step=1)
    m = st.number_input("Numbre colonnes (m)", min_value=1, value=3, step=1)

    # Input matrix in a grid-like format
    st.write("Entrer la matrice:")
    cost_matrix = []
    for i in range(n):
        cols = st.columns(m)
        row = []
        for j in range(m):
            with cols[j]:
                value = st.number_input(f"ligne {i+1}, colonne {j+1}", value=0, key=f"cell_{i}_{j}")
                row.append(value)
        cost_matrix.append(row)

    # Convert to numpy array
    cost_matrix = np.array(cost_matrix)

    # Convert rectangular matrix to square matrix
    square_matrix = make_square(cost_matrix)

    # Display the square matrix
    st.write("### la matrice carrée:")
    st.write(square_matrix)

    # Solve button
    if st.button("Solve"):
        try:
            # Solve the assignment problem using the Hungarian Algorithm
            assignment = hungarian_algorithm(square_matrix)

            # Calculate the total cost using the original cost matrix
            total_cost = 0
            for i, j in enumerate(assignment):
                if i < n and j < m:  # Only consider valid assignments within the original matrix dimensions
                    total_cost += cost_matrix[i, j]

            # Display the result
            st.write("### Resultat:")
            for i, j in enumerate(assignment):
                if i < n and j < m:  # Only show valid assignments within the original matrix dimensions
                    st.write(f"ligne {i+1} → colonne {j+1}")
            st.write(f"### Coût total: {total_cost}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Run the Streamlit app
if __name__ == "__main__":
    main()
