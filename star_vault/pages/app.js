/* ── StarLink Vault — Vue 3 SPA ──────────────────── */

const { createApp, ref, computed, onMounted, watch, nextTick } = Vue;

const app = createApp({
  setup() {
    // ── State ──────────────────────
    const data = ref(null);
    const loading = ref(true);
    const error = ref(null);
    const route = ref('/');
    const searchQuery = ref('');
    const filterLang = ref('');
    const groupBy = ref('category'); // category|language|maintenance|list

    // TODO filters
    const todoCategoryFilter = ref('');
    const todoPriorityFilter = ref('');
    const todoStatusFilter = ref(''); // ''|pending|done

    // ── Data loading ──────────────
    onMounted(async () => {
      try {
        const resp = await fetch('site-data.json');
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        data.value = await resp.json();
      } catch (e) {
        error.value = '无法加载 Vault 数据。请先运行 `star-vault sync --with-pages` 生成站点数据。';
        console.error(e);
      } finally {
        loading.value = false;
      }
    });

    // ── Hash routing ──────────────
    function onHash() {
      route.value = window.location.hash.slice(1) || '/';
    }
    onMounted(onHash);
    watch(route, (r) => {
      const hash = '#' + r;
      if (window.location.hash !== hash) window.location.hash = hash;
    });
    window.addEventListener('hashchange', onHash);

    function nav(path) { route.value = path; }

    // ── Computed ──────────────────

    const allNotes = computed(() => data.value?.notes ?? []);
    const stats = computed(() => data.value?.stats ?? { total: 0 });

    // Filter contexts
    const languages = computed(() => {
      const s = new Set();
      allNotes.value.forEach(n => { if (n.language) s.add(n.language); });
      return [...s].sort();
    });

    const categories = computed(() => {
      const s = new Set();
      allNotes.value.forEach(n => { if (n.category) s.add(n.category); });
      return [...s].sort();
    });

    const maintenances = computed(() => {
      const s = new Set();
      allNotes.value.forEach(n => { if (n.maintenance) s.add(n.maintenance); });
      return [...s].sort();
    });

    // Filtered list
    const filteredNotes = computed(() => {
      let list = allNotes.value;
      const q = searchQuery.value.trim().toLowerCase();
      if (q) {
        list = list.filter(n =>
          n.repo_full_name.toLowerCase().includes(q) ||
          (n.title && n.title.toLowerCase().includes(q)) ||
          (n.language && n.language.toLowerCase().includes(q)) ||
          n.topics.some(t => t.toLowerCase().includes(q)) ||
          (n.ai_tags && n.ai_tags.some(t => t.toLowerCase().includes(q)))
        );
      }
      if (filterLang.value) list = list.filter(n => n.language === filterLang.value);
      return list;
    });

    // ── Multi-dimension grouping ───
    const groupedNotes = computed(() => {
      const g = groupBy.value;
      const groups = {};
      const list = filteredNotes.value;

      if (g === 'category') {
        list.forEach(n => {
          const key = n.category || 'other';
          if (!groups[key]) groups[key] = [];
          groups[key].push(n);
        });
        // Sort: known categories first
        const order = ['tool', 'lib', 'framework', 'tutorial', 'demo', 'article', 'other'];
        return Object.fromEntries(
          order.filter(k => groups[k]).map(k => [k, groups[k]])
            .concat(Object.entries(groups).filter(([k]) => !order.includes(k)))
        );
      }

      if (g === 'language') {
        list.forEach(n => {
          const key = n.language || 'other';
          if (!groups[key]) groups[key] = [];
          groups[key].push(n);
        });
        return Object.fromEntries(
          Object.entries(groups).sort((a, b) => b[1].length - a[1].length)
        );
      }

      if (g === 'maintenance') {
        list.forEach(n => {
          const key = n.maintenance || 'unknown';
          if (!groups[key]) groups[key] = [];
          groups[key].push(n);
        });
        const order = ['active', 'stale', 'archived', 'unknown'];
        return Object.fromEntries(
          order.filter(k => groups[k]).map(k => [k, groups[k]])
        );
      }

      // list (default, backward compat)
      list.forEach(n => {
        const key = n.list_name || '_uncategorized';
        if (!groups[key]) groups[key] = [];
        groups[key].push(n);
      });
      return Object.fromEntries(
        Object.entries(groups).sort((a, b) => a[0].localeCompare(b[0]))
      );
    });

    const groupKeys = computed(() => Object.keys(groupedNotes.value));

    const currentNote = computed(() => {
      const m = route.value.match(/^\/repo\/(.+)/);
      if (!m) return null;
      return allNotes.value.find(n => n.slug === m[1]) || null;
    });

    // ── TODO with localStorage persistence ──
    const doneCache = ref({});

    function loadDoneCache() {
      try {
        const raw = localStorage.getItem('starlink_todo_done');
        if (raw) doneCache.value = JSON.parse(raw);
      } catch {}
    }
    function saveDoneCache() {
      try {
        localStorage.setItem('starlink_todo_done', JSON.stringify(doneCache.value));
      } catch {}
    }

    function todoKey(item) {
      return item.slug + '::' + item.text;
    }
    function isDone(item) { return doneCache.value[todoKey(item)] === true; }
    function toggleDone(item) {
      const k = todoKey(item);
      if (doneCache.value[k]) {
        delete doneCache.value[k];
      } else {
        doneCache.value[k] = true;
      }
      saveDoneCache();
    }

    loadDoneCache();

    // Tagged TODO items (with computed urgency from item order)
    const allTodos = computed(() => {
      const todos = [];
      allNotes.value.forEach(n => {
        if (!n.todo_items || !n.todo_items.length) return;
        n.todo_items.forEach((t, idx) => {
          todos.push({
            text: t.text,
            slug: n.slug,
            repo: n.repo_full_name,
            category: n.category || '',
            language: n.language || '',
            rating: n.rating || 0,
            // urgency: use priority if set, else default 3
            urgency: t.priority || 3,
            done: isDone({ slug: n.slug, text: t.text }),
          });
        });
      });
      return todos;
    });

    // Filtered todos
    const filteredTodos = computed(() => {
      let list = allTodos.value;
      if (todoCategoryFilter.value) {
        list = list.filter(t => t.category === todoCategoryFilter.value);
      }
      if (todoPriorityFilter.value) {
        const p = parseInt(todoPriorityFilter.value);
        list = list.filter(t => t.urgency === p);
      }
      if (todoStatusFilter.value === 'pending') {
        list = list.filter(t => !t.done);
      } else if (todoStatusFilter.value === 'done') {
        list = list.filter(t => t.done);
      }
      return list;
    });

    // Priority-grouped todos
    const todoGroups = computed(() => {
      const list = filteredTodos.value;
      const high = list.filter(t => t.urgency <= 2);
      const mid = list.filter(t => t.urgency === 3);
      const low = list.filter(t => t.urgency >= 4);
      const result = [];
      if (high.length) result.push({ label: '高优先级', key: 'high', items: high });
      if (mid.length) result.push({ label: '中优先级', key: 'mid', items: mid });
      if (low.length) result.push({ label: '低优先级', key: 'low', items: low });
      return result;
    });

    const todoCount = computed(() => ({
      high: todoGroups.value.find(g => g.key === 'high')?.items.length || 0,
      mid: todoGroups.value.find(g => g.key === 'mid')?.items.length || 0,
      low: todoGroups.value.find(g => g.key === 'low')?.items.length || 0,
    }));

    // ── Relations ──────────────────
    const allRelations = computed(() => {
      const clusters = {};
      allNotes.value.forEach(n => {
        if (!n.relations || !n.relations.length) return;
        const key = n.relations.map(r => r.relation_type).sort().join(',');
        if (!clusters[key]) clusters[key] = { type: key, repos: [], relations: [] };
        clusters[key].repos.push(n.repo_full_name);
        clusters[key].relations.push(...n.relations.map(r => ({
          ...r,
          source: n.repo_full_name,
        })));
      });
      return Object.values(clusters).sort((a, b) => b.repos.length - a.repos.length);
    });

    // ── Recommendation view ─────────
    const recommendedNotes = computed(() => {
      return [...allNotes.value]
        .filter(n => n.rating >= 1)
        .sort((a, b) => {
          // Score: rating * 2, tie-break by todo count
          const scoreA = (a.rating || 0) * 2 - (a.todo_items?.length || 0) * 0.1;
          const scoreB = (b.rating || 0) * 2 - (b.todo_items?.length || 0) * 0.1;
          return scoreB - scoreA;
        })
        .slice(0, 20);
    });

    // ── Helpers ────────────────────
    const langColors = {
      'Python': '#3572A5', 'JavaScript': '#F7DF1E', 'TypeScript': '#3178C6',
      'HTML': '#E34F26', 'CSS': '#563D7C', 'Go': '#00ADD8', 'Rust': '#DEA584',
      'Java': '#B07219', 'C': '#555555', 'C++': '#F34B7F', 'C#': '#178600',
      'Ruby': '#701516', 'PHP': '#4F5D95', 'Swift': '#F05138', 'Kotlin': '#A97BFF',
      'Scala': '#C22D40', 'Shell': '#89E051', 'Jupyter Notebook': '#DA5B0B',
      'Vue': '#4FC08D', 'Svelte': '#FF3E00', 'Dart': '#00B4AB',
    };
    function langColor(lang) { return langColors[lang] || '#8b949e'; }

    const categoryIcons = {
      'tool': '🔧', 'lib': '📦', 'tutorial': '📖',
      'demo': '🎮', 'article': '📝', 'framework': '🏗️', 'other': '📁',
    };
    function catIcon(cat) { return categoryIcons[cat] || ''; }

    function ratingStars(r) {
      if (!r || r < 1) return '';
      return '★'.repeat(r) + '☆'.repeat(5 - r);
    }

    const maintColor = {
      'active': 'var(--green)',
      'stale': 'var(--yellow)',
      'archived': 'var(--red)',
    };
    function maintStyle(m) { return { color: maintColor[m] || 'var(--text-muted)' }; }

    function toSlug(name) { return name.replace(/\//g, '.').toLowerCase(); }

    // ── Exports ────────────────────
    return {
      data, loading, error, route, searchQuery, filterLang,
      groupBy,
      todoCategoryFilter, todoPriorityFilter, todoStatusFilter,
      allNotes, stats, languages, categories, maintenances,
      filteredNotes, groupedNotes, groupKeys,
      currentNote,
      allTodos, filteredTodos, todoGroups, todoCount,
      allRelations, recommendedNotes,
      nav, renderMd, highlightBlocks, langColor, toSlug,
      catIcon, ratingStars, maintStyle,
      todoKey, isDone, toggleDone,
    };
  },

  // ── Markdown helpers (outside setup) ──
  methods: {
    renderMd(text) {
      if (!text) return '';
      const html = marked.parse(text, { breaks: true, gfm: true });
      return DOMPurify.sanitize(html);
    },
    highlightBlocks() {
      nextTick(() => {
        document.querySelectorAll('.markdown-body pre code').forEach(block => {
          hljs.highlightElement(block);
        });
      });
    },
  },

  watch: {
    currentNote() { this.highlightBlocks(); },
  },
});

app.mount('#app');
