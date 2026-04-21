import json

def save_json(kg, filename="knowledge_graph.json"):
    """Save knowledge graph as JSON."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(kg, f, indent=2, ensure_ascii=False)
    print(f" {filename}: JSON knowledge graph")

def save_triplets_txt(kg, filename="triplets.txt"):
    """Save triplets as simple text file."""
    with open(filename, 'w', encoding='utf-8') as f:
        
        for triplet in kg["triplets"]:
            f.write(f"({triplet['subject']}, {triplet['predicate']}, {triplet['object']})\n")
        
        f.write(f"\n\n--- STATISTICS ---\n")
        f.write(f"Total Entities: {kg['statistics']['total_entities']}\n")
        f.write(f"Total Triplets: {kg['statistics']['total_triplets']}\n")
    
    print(f"{filename}: Triple list")

def visualize_ascii(kg):
    """Display ASCII visualization of the knowledge graph."""
    # Group by subject
    by_subject = {}
    for triplet in kg["triplets"]:
        subj = triplet["subject"]
        if subj not in by_subject:
            by_subject[subj] = []
        by_subject[subj].append((triplet["predicate"], triplet["object"]))
    
    print("\n" + "="*50)
    print("ASCII KNOWLEDGE GRAPH VISUALIZATION")
    print("="*50)
    
    for subject, relations in by_subject.items():
        print(f"\n {subject}")
        for i, (pred, obj) in enumerate(relations):
            prefix = "└─" if i == len(relations) - 1 else "├─"
            # Truncate long objects
            obj_display = obj[:50] + "..." if len(obj) > 50 else obj
            print(f"   {prefix} {pred} → {obj_display}")

def visualize_html(kg, filename="knowledge_graph.html"):
    """Create interactive HTML visualization using D3.js."""
    
    # Prepare data
    nodes = {}
    links = []
    
    for triplet in kg["triplets"]:
        nodes[triplet["subject"]] = {"id": triplet["subject"]}
        nodes[triplet["object"]] = {"id": triplet["object"]}
        links.append({
            "source": triplet["subject"],
            "target": triplet["object"],
            "label": triplet["predicate"]
        })
    
    # Get source text preview for title
    source_preview = kg["source_text"][:50] + "..." if len(kg["source_text"]) > 50 else kg["source_text"]
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Knowledge Graph - {source_preview}</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; overflow: hidden; background: #f5f5f5; }}
        #header {{
            position: absolute;
            top: 20px;
            left: 20px;
            background: white;
            padding: 10px 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 10;
            font-size: 14px;
        }}
        #stats {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: white;
            padding: 8px 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 10;
            font-size: 12px;
            font-family: monospace;
        }}
        #controls {{
            position: absolute;
            bottom: 20px;
            right: 20px;
            background: white;
            padding: 8px 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 10;
            font-size: 12px;
            display: flex;
            gap: 10px;
        }}
        button {{
            padding: 5px 10px;
            cursor: pointer;
            border: 1px solid #ccc;
            background: white;
            border-radius: 4px;
        }}
        button:hover {{ background: #f0f0f0; }}
        .tooltip {{
            position: absolute;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
            pointer-events: none;
            z-index: 20;
        }}
    </style>
</head>
<body>
    <div id="header">
        <strong>Knowledge Graph</strong><br>
        <span style="font-size: 11px; color: #666;">{source_preview}</span><br>
        <span style="font-size: 10px; color: #999;">Drag nodes to rearrange | Hover for details</span>
    </div>
    <div id="stats">
        <strong>Statistics</strong><br>
        Nodes: {len(nodes)} | Relationships: {len(links)}
    </div>
    <div id="controls">
        <button onclick="resetZoom()">Reset View</button>
        <button onclick="toggleLabels()">Toggle Labels</button>
    </div>
    <div id="graph"></div>
    
    <script>
        const data = {{
            nodes: {list(nodes.values())},
            links: {links}
        }};
        
        const width = window.innerWidth;
        const height = window.innerHeight;
        
        const svg = d3.select("#graph")
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .call(d3.zoom().on("zoom", (event) => {{
                g.attr("transform", event.transform);
            }}))
            .append("g");
        
        let g = svg;
        
        const simulation = d3.forceSimulation(data.nodes)
            .force("link", d3.forceLink(data.links).id(d => d.id).distance(120))
            .force("charge", d3.forceManyBody().strength(-200))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collision", d3.forceCollide().radius(40));
        
        // Create tooltip
        const tooltip = d3.select("body").append("div")
            .attr("class", "tooltip")
            .style("opacity", 0);
        
        // Draw links
        const link = g.append("g")
            .selectAll("line")
            .data(data.links)
            .enter()
            .append("line")
            .attr("stroke", "#999")
            .attr("stroke-width", 1.5)
            .attr("stroke-opacity", 0.6);
        
        // Draw link labels
        const linkLabel = g.append("g")
            .selectAll("text")
            .data(data.links)
            .enter()
            .append("text")
            .attr("font-size", "9px")
            .attr("fill", "#666")
            .attr("text-anchor", "middle")
            .text(d => d.label);
        
        // Draw nodes
        const node = g.append("g")
            .selectAll("g")
            .data(data.nodes)
            .enter()
            .append("g")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));
        
        // Node circles with color coding
        node.append("circle")
            .attr("r", 22)
            .attr("fill", d => {{
                if (d.id === "Alan Turing") return "#FF6B6B";
                if (d.id.includes("date") || /\\d{{4}}/.test(d.id)) return "#FFE5B4";
                if (d.id.includes("London") || d.id.includes("Wilmslow")) return "#B4FFB4";
                if (d.id.includes("University")) return "#B4D4FF";
                if (d.id.includes("Machine") || d.id.includes("Theory")) return "#D4B4FF";
                return "#87CEEB";
            }})
            .attr("stroke", "#333")
            .attr("stroke-width", 1.5)
            .on("mouseover", function(event, d) {{
                tooltip.transition().duration(200).style("opacity", 0.9);
                tooltip.html(`<strong>${{d.id}}</strong>`)
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 10) + "px");
                d3.select(this).attr("stroke-width", 3);
            }})
            .on("mouseout", function() {{
                tooltip.transition().duration(500).style("opacity", 0);
                d3.select(this).attr("stroke-width", 1.5);
            }});
        
        // Node labels
        const nodeLabel = node.append("text")
            .attr("dy", 4)
            .attr("text-anchor", "middle")
            .attr("font-size", "10px")
            .attr("font-weight", "bold")
            .attr("fill", "#333")
            .text(d => d.id.length > 18 ? d.id.substring(0, 15) + "..." : d.id);
        
        let labelsVisible = true;
        function toggleLabels() {{
            labelsVisible = !labelsVisible;
            nodeLabel.style("opacity", labelsVisible ? 1 : 0);
            linkLabel.style("opacity", labelsVisible ? 1 : 0);
        }}
        
        function resetZoom() {{
            g.transition().duration(750).call(
                d3.zoom().transform,
                d3.zoomIdentity
            );
        }}
        
        simulation.on("tick", () => {{
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
            
            linkLabel
                .attr("x", d => (d.source.x + d.target.x) / 2)
                .attr("y", d => (d.source.y + d.target.y) / 2 - 5);
            
            node.attr("transform", d => `translate(${{d.x}},${{d.y}})`);
        }});
        
        function dragstarted(event, d) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }}
        
        function dragged(event, d) {{
            d.fx = event.x;
            d.fy = event.y;
        }}
        
        function dragended(event, d) {{
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }}
        
        window.addEventListener('resize', () => {{
            const newWidth = window.innerWidth;
            const newHeight = window.innerHeight;
            svg.attr("width", newWidth).attr("height", newHeight);
            simulation.force("center", d3.forceCenter(newWidth / 2, newHeight / 2));
            simulation.alpha(0.3).restart();
        }});
    </script>
</body>
</html>'''
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f" {filename}: Interactive HTML visualization")

def visualize_dot(kg, filename="knowledge_graph.dot"):
    """Create DOT format for Graphviz."""
    
    lines = ['digraph KnowledgeGraph {']
    lines.append('    rankdir=LR;')
    lines.append('    node [shape=box, style=filled, fillcolor=lightblue];')
    lines.append('')
    
    # Add nodes
    nodes_added = set()
    for triplet in kg["triplets"]:
        for node in [triplet["subject"], triplet["object"]]:
            if node not in nodes_added:
                node_clean = node.replace('"', '\\"')
                lines.append(f'    "{node_clean}";')
                nodes_added.add(node)
    
    lines.append('')
    
    # Add edges
    for triplet in kg["triplets"]:
        subj = triplet["subject"].replace('"', '\\"')
        obj = triplet["object"].replace('"', '\\"')
        pred = triplet["predicate"]
        lines.append(f'    "{subj}" -> "{obj}" [label="{pred}"];')
    
    lines.append('}')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f" {filename}: Graphviz DOT file")

def print_summary(kg):
    
    print("\nENTITIES:")
    for ent in kg["entities"]:
        if ent.get("disambiguated"):
            print(f"  • {ent['resolved_to']} ({ent.get('type', ent['label'])}) ← from '{ent['original_text']}'")
        else:
            print(f"  • {ent['resolved_to']} ({ent.get('type', ent['label'])})")
    
    print("\nRELATIONSHIPS (Triplets):")
    for triplet in kg["triplets"]:
        print(f"  • ({triplet['subject']}, {triplet['predicate']}, {triplet['object']})")
    
    print(f"\nSTATISTICS:")
    print(f"  • Total entities: {kg['statistics']['total_entities']}")
    print(f"  • Total relationships: {kg['statistics']['total_triplets']}")
    print(f"  • Entity types: {kg['statistics']['entity_types']}")
    print("="*50 + "\n")