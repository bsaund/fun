import plotly.graph_objects as go
import numpy as np
from typing import List, Tuple

def generate_data() -> Tuple[List[float], List[float]]:
    """Generate scatter plot data with most points on diagonal, some off diagonal"""
    x_points: List[float] = []
    y_points: List[float] = []
    
    # Generate points mostly on the diagonal (y ≈ x)
    # Add some noise to make it realistic
    np.random.seed(42)  # For reproducibility
    
    # Most points on diagonal (with small random noise)
    num_diagonal: int = 50
    x_diagonal = np.linspace(0, 10, num_diagonal)
    y_diagonal = x_diagonal + np.random.normal(0, 0.3, num_diagonal)
    
    # Some points off diagonal
    num_off_diagonal: int = 15
    num_above: int = num_off_diagonal // 2
    num_below: int = num_off_diagonal - num_above
    
    # Points above diagonal
    x_off_above = np.random.uniform(0, 10, num_above)
    y_off_above = x_off_above + np.random.uniform(1, 3, num_above)
    
    # Points below diagonal
    x_off_below = np.random.uniform(0, 10, num_below)
    y_off_below = x_off_below - np.random.uniform(1, 3, num_below)
    
    # Combine all points
    x_points = np.concatenate([x_diagonal, x_off_above, x_off_below]).tolist()
    y_points = np.concatenate([y_diagonal, y_off_above, y_off_below]).tolist()
    
    return x_points, y_points

def plot_scatter_with_shading(x_data: List[float], y_data: List[float]) -> None:
    """
    Create a scatter plot with shaded regions:
    - Red shading below y = 0.8x
    - Green shading above y = 1.2x
    """
    # Create the figure
    fig = go.Figure()
    
    # Define x range for shading regions
    x_range = np.linspace(0, max(x_data) * 1.1, 100)
    
    # Calculate boundary lines
    y_lower = 0.8 * x_range  # Below this line should be red
    y_upper = 1.2 * x_range  # Above this line should be green
    
    # Add red shading below y = 0.8x
    # We'll shade from y = 0 to y = 0.8x
    fig.add_trace(go.Scatter(
        x=np.concatenate([x_range, x_range[::-1]]),
        y=np.concatenate([y_lower, np.zeros_like(x_range)]),
        fill='tozeroy',
        fillcolor='rgba(255, 0, 0, 0.3)',
        line=dict(color='rgba(255, 0, 0, 0)'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add green shading above y = 1.2x
    # Create a polygon that fills above the line
    max_y_shade = max(y_data) * 1.2 if y_data else 15
    fig.add_trace(go.Scatter(
        x=np.concatenate([x_range, x_range[::-1]]),
        y=np.concatenate([y_upper, np.full_like(x_range, max_y_shade)]),
        fill='toself',
        fillcolor='rgba(0, 255, 0, 0.3)',
        line=dict(color='rgba(0, 255, 0, 0)'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add boundary lines
    fig.add_trace(go.Scatter(
        x=x_range,
        y=y_lower,
        mode='lines',
        name='y = 0.8x',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=x_range,
        y=y_upper,
        mode='lines',
        name='y = 1.2x',
        line=dict(color='green', width=2, dash='dash')
    ))
    
    # Add diagonal reference line (y = x)
    fig.add_trace(go.Scatter(
        x=x_range,
        y=x_range,
        mode='lines',
        name='y = x (diagonal)',
        line=dict(color='blue', width=1, dash='dot')
    ))
    
    # Add scatter points
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode='markers',
        name='Discomfort',
        marker=dict(
            size=8,
            color='rgba(50, 50, 200, 0.6)',
            line=dict(width=1, color='rgba(50, 50, 200, 0.8)')
        )
    ))
    
    # Update layout
    fig.update_layout(
        title='Scatter Plot with Shaded Regions',
        xaxis_title='human',
        yaxis_title='AV',
        xaxis=dict(range=[0, max(x_data) * 1.1]),
        yaxis=dict(range=[min(min(y_data), 0), max(y_data) * 1.1]),
        hovermode='closest',
        template='plotly_white',
        width=800,
        height=600
    )
    
    # Show the plot
    fig.show()

def main() -> None:
    """Main function to generate and plot data"""
    x_data, y_data = generate_data()
    plot_scatter_with_shading(x_data, y_data)

if __name__ == "__main__":
    main()
