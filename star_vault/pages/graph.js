/* ── StarLink Relation Graph (vis-network) ──────────── */

/**
 * 从 allNotes 和 allRelations 构建 vis-network 图。
 * 在 #graph-container div 就绪后调用。
 */
function buildGraph(notes, relationsList) {
  const container = document.getElementById('graph-container');
  if (!container || typeof vis === 'undefined') return;

  // ── Build node map ───────────────────
  const noteMap = {};
  notes.forEach(n => { noteMap[n.repo_full_name] = n; });

  // ── Count connections per node ──────
  const connCount = {};
  relationsList.forEach(cluster => {
    cluster.relations.forEach(rel => {
      connCount[rel.source] = (connCount[rel.source] || 0) + 1;
      connCount[rel.target_slug] = (connCount[rel.target_slug] || 0) + 1;
    });
  });

  // ── Build nodes ─────────────────────
  const relatedNames = new Set();
  relationsList.forEach(c => c.relations.forEach(r => {
    relatedNames.add(r.source);
    relatedNames.add(r.target_slug);
  }));

  // Only show repos that have relations
  const nodes = [];
  notes.forEach(n => {
    if (!relatedNames.has(n.repo_full_name)) return;
    const count = connCount[n.repo_full_name] || 0;
    const size = Math.min(40, Math.max(12, 10 + count * 3));
    const borderColor = {
      'active': '#3fb950',
      'stale': '#d29922',
      'archived': '#f85149',
    }[n.maintenance] || '#8b949e';

    nodes.push({
      id: n.repo_full_name,
      label: n.repo_full_name,
      title: makeTooltip(n),
      size: size,
      color: {
        background: langColors[n.language] || '#8b949e',
        border: borderColor,
        highlight: { background: '#58a6ff', border: '#1f6feb' },
      },
      font: { color: '#e6edf3', size: 11, face: '-apple-system, sans-serif' },
      borderWidth: count > 5 ? 3 : 2,
      shape: 'dot',
      slug: n.slug,
    });
  });

  // ── Build edges ─────────────────────
  const edges = [];
  const edgeColors = {
    'SIMILAR_TOPICS': '#58a6ff',
    'ALTERNATIVE': '#3fb950',
    'DEPENDS_ON': '#d29922',
  };
  const edgeDash = {
    'SIMILAR_TOPICS': false,
    'ALTERNATIVE': true,
    'DEPENDS_ON': false,
  };

  relationsList.forEach(cluster => {
    cluster.relations.forEach(rel => {
      const targetFull = rel.target_slug.replace(/\./g, '/');
      const sourceFull = rel.source;
      if (!nodeMap[sourceFull] || !nodeMap[targetFull]) return;
      edges.push({
        from: sourceFull,
        to: targetFull,
        color: {
          color: edgeColors[rel.relation_type] || '#30363d',
          opacity: Math.min(1, Math.max(0.2, rel.confidence)),
        },
        width: Math.max(0.5, rel.confidence * 2),
        dashes: edgeDash[rel.relation_type] || false,
        title: `${rel.relation_type} (${(rel.confidence * 100).toFixed(0)}%)`,
      });
    });
  });

  // ── Cluster by category ─────────────
  const categoryOrder = ['tool', 'framework', 'lib', 'tutorial', 'demo', 'article', 'other'];
  const catPositions = {};
  categoryOrder.forEach((cat, i) => {
    const catNotes = notes.filter(n => (n.category || 'other') === cat && relatedNames.has(n.repo_full_name));
    catNotes.forEach((n, j) => {
      catPositions[n.repo_full_name] = {
        x: (i - 3) * 250 + (j % 5 - 2) * 60,
        y: Math.floor(j / 5) * 80 - (catNotes.length / 5 / 2) * 80,
      };
    });
  });

  // ── Options ────────────────────────
  const options = {
    nodes: { scaling: { min: 12, max: 40 } },
    edges: { smooth: { type: 'continuous' } },
    physics: {
      solver: 'forceAtlas2Based',
      forceAtlas2Based: {
        gravitationalConstant: -40,
        centralGravity: 0.005,
        springLength: 180,
        springConstant: 0.02,
        damping: 0.4,
        avoidOverlap: 0.5,
      },
      stabilization: { iterations: 200 },
    },
    interaction: {
      hover: true,
      tooltipDelay: 100,
      zoomView: true,
      dragView: true,
      multiselect: false,
    },
    layout: { improvedLayout: true },
  };

  // ── Render ─────────────────────────
  const data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };
  const network = new vis.Network(container, data, options);

  // ── Click handler → repo detail ────
  network.on('click', function (params) {
    if (params.nodes.length > 0) {
      const nodeId = params.nodes[0];
      const note = notes.find(n => n.repo_full_name === nodeId);
      if (note) {
        window.location.hash = '#/repo/' + note.slug;
      }
    }
  });

  return network;
}

/** Generate hover tooltip HTML */
function makeTooltip(n) {
  const stars = (n.rating && n.rating >= 1)
    ? '★'.repeat(n.rating) + '☆'.repeat(5 - n.rating)
    : '';
  const catIcons = {tool:'&#x1F527;',lib:'&#x1F4E6;',tutorial:'&#x1F4D6;',demo:'&#x1F3AE;',article:'&#x1F4DD;',framework:'&#x1F3D7;&#xFE0F;',other:'&#x1F4C1;'};
  const cat = n.category ? `  ${catIcons[n.category] || ''} ${n.category}` : '';
  return `<div style="font-size:13px;line-height:1.5">
    <strong>${n.repo_full_name}</strong><br>
    ${stars ? stars + ' ' : ''}${n.language || ''}${cat}<br>
    ${n.maintenance ? n.maintenance : ''}
    ${(n.todo_items && n.todo_items.length) ? ' · ' + n.todo_items.length + ' TODO' : ''}
    ${n.ai_summary ? '<br><span style="color:#8b949e;font-size:11px">' + n.ai_summary.slice(0, 80) + '…</span>' : ''}
  </div>`;
}
