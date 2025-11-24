"""
Performance and Error Analysis - Bar Graph Generator
Generates publication-quality bar graphs for IEEE paper
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Set style for publication quality
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 12
plt.rcParams['font.family'] = 'serif'

def create_performance_comparison_graph():
    """
    Create comprehensive performance comparison bar graph
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # ==================== GRAPH 1: Component Accuracy ====================
    components = ['Embedding\nRetrieval', 'Summarization', 'Quiz\nGeneration', 
                  'Classification', 'Recommendations', 'End-to-End\nPipeline']
    accuracy = [83.7, 87.5, 95.1, 91.2, 93.4, 95.0]
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
    
    bars1 = ax1.bar(components, accuracy, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Accuracy (%)', fontsize=14, fontweight='bold')
    ax1.set_title('(a) Component-wise Accuracy Comparison', fontsize=16, fontweight='bold')
    ax1.set_ylim([0, 100])
    ax1.axhline(y=90, color='red', linestyle='--', linewidth=2, label='90% threshold')
    ax1.grid(axis='y', alpha=0.3)
    ax1.legend(fontsize=10)
    
    # Add value labels on bars
    for bar, acc in zip(bars1, accuracy):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{acc}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # ==================== GRAPH 2: Error Rate Analysis ====================
    error_types = ['Summarization\nErrors', 'Quiz\nHallucinations', 'Parsing\nErrors', 
                   'Classification\nMismatches', 'Recommendation\nIssues']
    error_rates = [12.5, 4.9, 3.0, 8.8, 6.6]  # Error rates in percentage
    
    bars2 = ax2.bar(error_types, error_rates, color='#e74c3c', alpha=0.7, 
                    edgecolor='darkred', linewidth=1.5)
    ax2.set_ylabel('Error Rate (%)', fontsize=14, fontweight='bold')
    ax2.set_title('(b) Error Rate Distribution by Component', fontsize=16, fontweight='bold')
    ax2.set_ylim([0, 15])
    ax2.axhline(y=5, color='green', linestyle='--', linewidth=2, label='5% acceptable threshold')
    ax2.grid(axis='y', alpha=0.3)
    ax2.legend(fontsize=10)
    
    # Add value labels
    for bar, err in zip(bars2, error_rates):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                f'{err}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # ==================== GRAPH 3: Performance vs Baseline ====================
    methods = ['Baseline\nExtractive', 'Baseline\nRandom Quiz', 'Baseline\nFixed Rec', 'Antigravity\n(Ours)']
    summarization_perf = [65.2, 0, 0, 87.5]
    quiz_perf = [0, 42.1, 0, 95.1]
    rec_perf = [0, 0, 50.0, 93.4]
    
    x = np.arange(len(methods))
    width = 0.25
    
    bars3_1 = ax3.bar(x - width, summarization_perf, width, label='Summarization', 
                      color='#3498db', alpha=0.8, edgecolor='black')
    bars3_2 = ax3.bar(x, quiz_perf, width, label='Quiz Relevance', 
                      color='#2ecc71', alpha=0.8, edgecolor='black')
    bars3_3 = ax3.bar(x + width, rec_perf, width, label='Recommendations', 
                      color='#f39c12', alpha=0.8, edgecolor='black')
    
    ax3.set_ylabel('Performance (%)', fontsize=14, fontweight='bold')
    ax3.set_title('(c) Antigravity vs Baseline Methods', fontsize=16, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(methods)
    ax3.set_ylim([0, 105])
    ax3.legend(fontsize=11, loc='upper left')
    ax3.grid(axis='y', alpha=0.3)
    
    # Add improvement annotations
    ax3.annotate('+22.3%', xy=(3, 87.5), xytext=(3, 95), 
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=12, color='red', fontweight='bold')
    ax3.annotate('+53.0%', xy=(3, 95.1), xytext=(2.5, 105), 
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=12, color='red', fontweight='bold')
    
    # ==================== GRAPH 4: Response Time Comparison ====================
    operations = ['Upload &\nProcess', 'Summarize', 'Generate\nQuiz', 'Grade\nQuiz', 'Total\nPipeline']
    response_times = [2.3, 4.2, 3.5, 0.08, 10.1]
    std_devs = [0.8, 1.1, 0.9, 0.02, 2.0]
    
    bars4 = ax4.bar(operations, response_times, yerr=std_devs, capsize=5,
                    color='#9b59b6', alpha=0.8, edgecolor='black', linewidth=1.5)
    ax4.set_ylabel('Time (seconds)', fontsize=14, fontweight='bold')
    ax4.set_title('(d) Average Response Time per Operation', fontsize=16, fontweight='bold')
    ax4.set_ylim([0, 14])
    ax4.axhline(y=5, color='green', linestyle='--', linewidth=2, label='5s target')
    ax4.grid(axis='y', alpha=0.3)
    ax4.legend(fontsize=10)
    
    # Add value labels
    for bar, time in zip(bars4, response_times):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{time}s', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Overall adjustments
    plt.suptitle('ANTIGRAVITY SYSTEM - Performance and Error Analysis', 
                 fontsize=20, fontweight='bold', y=0.995)
    plt.tight_layout(rect=[0, 0.03, 1, 0.98])
    
    # Save with high DPI for publication
    plt.savefig('performance_analysis_graph.png', dpi=300, bbox_inches='tight')
    plt.savefig('performance_analysis_graph.pdf', bbox_inches='tight')  # For LaTeX
    print("✅ Saved: performance_analysis_graph.png (300 DPI)")
    print("✅ Saved: performance_analysis_graph.pdf (Vector format for IEEE)")
    
    plt.show()

def create_accuracy_comparison_graph():
    """
    Create detailed accuracy comparison with error bars
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Data
    metrics = ['Embedding\nRetrieval\n@k=5', 'Summarization\nQuality', 
               'Quiz\nRelevance', 'Classification\nAccuracy', 
               'Recommendation\nMatch', 'User\nSatisfaction\n(×20)']
    
    training_acc = [85.2, 89.0, 91.2, 100.0, 100.0, 88.0]
    validation_acc = [83.7, 87.5, 95.1, 91.2, 93.4, 88.0]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, training_acc, width, label='Training/Baseline', 
                   color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
    bars2 = ax.bar(x + width/2, validation_acc, width, label='Validation/Final', 
                   color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1.5)
    
    ax.set_ylabel('Accuracy (%)', fontsize=16, fontweight='bold')
    ax.set_xlabel('Performance Metrics', fontsize=16, fontweight='bold')
    ax.set_title('Training vs Validation Accuracy Across All Metrics', 
                 fontsize=18, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=12)
    ax.set_ylim([0, 105])
    ax.legend(fontsize=14, loc='lower right')
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Add 90% threshold line
    ax.axhline(y=90, color='red', linestyle='--', linewidth=2, alpha=0.7, 
               label='90% Acceptable Threshold')
    ax.legend(fontsize=12)
    
    plt.tight_layout()
    plt.savefig('training_validation_accuracy.png', dpi=300, bbox_inches='tight')
    plt.savefig('training_validation_accuracy.pdf', bbox_inches='tight')
    print("✅ Saved: training_validation_accuracy.png")
    print("✅ Saved: training_validation_accuracy.pdf")
    
    plt.show()

def create_scalability_graph():
    """
    Create scalability performance graph
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Graph 1: Concurrent Users vs Response Time
    users = [1, 10, 25, 50, 75, 100]
    response_time = [3.2, 3.2, 4.1, 5.1, 7.3, 8.7]
    success_rate = [100, 100, 99, 98, 95, 92]
    
    ax1_twin = ax1.twinx()
    
    line1 = ax1.plot(users, response_time, 'o-', linewidth=3, markersize=10, 
                     color='#e74c3c', label='Response Time')
    ax1.fill_between(users, response_time, alpha=0.3, color='#e74c3c')
    ax1.set_xlabel('Concurrent Users', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Response Time (seconds)', fontsize=14, fontweight='bold', color='#e74c3c')
    ax1.tick_params(axis='y', labelcolor='#e74c3c')
    ax1.set_title('(a) Scalability: Response Time vs Load', fontsize=16, fontweight='bold')
    ax1.grid(alpha=0.3)
    
    line2 = ax1_twin.plot(users, success_rate, 's-', linewidth=3, markersize=10, 
                          color='#2ecc71', label='Success Rate')
    ax1_twin.set_ylabel('Success Rate (%)', fontsize=14, fontweight='bold', color='#2ecc71')
    ax1_twin.tick_params(axis='y', labelcolor='#2ecc71')
    ax1_twin.set_ylim([85, 105])
    
    # Graph 2: Document Size vs Processing Time
    doc_sizes = ['1-10\npages', '11-20\npages', '21-30\npages', '31-40\npages', '41-50\npages']
    processing_time = [6.5, 8.2, 10.5, 13.1, 15.8]
    
    bars = ax2.bar(doc_sizes, processing_time, color='#9b59b6', alpha=0.8, 
                   edgecolor='black', linewidth=1.5)
    ax2.set_xlabel('Document Size', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Total Processing Time (seconds)', fontsize=14, fontweight='bold')
    ax2.set_title('(b) Document Size Impact on Processing', fontsize=16, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar, time in zip(bars, processing_time):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                f'{time}s', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('scalability_analysis.png', dpi=300, bbox_inches='tight')
    plt.savefig('scalability_analysis.pdf', bbox_inches='tight')
    print("✅ Saved: scalability_analysis.png")
    print("✅ Saved: scalability_analysis.pdf")
    
    plt.show()

if __name__ == "__main__":
    print("Generating Performance and Error Analysis Graphs...")
    print("=" * 60)
    
    # Generate all graphs
    create_performance_comparison_graph()
    print("\n" + "=" * 60)
    create_accuracy_comparison_graph()
    print("\n" + "=" * 60)
    create_scalability_graph()
    
    print("\n" + "=" * 60)
    print("✅ All graphs generated successfully!")
    print("\nGenerated files:")
    print("  📊 performance_analysis_graph.png (4-panel comprehensive)")
    print("  📊 performance_analysis_graph.pdf (vector format)")
    print("  📊 training_validation_accuracy.png")
    print("  📊 training_validation_accuracy.pdf")
    print("  📊 scalability_analysis.png")
    print("  📊 scalability_analysis.pdf")
    print("\nThese graphs are publication-ready for IEEE papers!")
