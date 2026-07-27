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
    const filterStatus = ref('');

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

    const languages = computed(() => {
      const s = new Set();
      allNotes.value.forEach(n => { if (n.language) s.add(n.language); });
      return [...s].sort();
    });

    const filteredNotes = computed(() => {
      let list = allNotes.value;
      const q = searchQuery.value.trim().toLowerCase();
      if (q) {
        list = list.filter(n =>
          n.repo_full_name.toLowerCase().includes(q) ||
          (n.title && n.title.toLowerCase().includes(q)) ||
          (n.language && n.language.toLowerCase().includes(q)) ||
          n.topics.some(t => t.toLowerCase().includes(q))
        );
      }
      if (filterLang.value) list = list.filter(n => n.language === filterLang.value);
      if (filterStatus.value) list = list.filter(n => n.status === filterStatus.value);
      return list;
    });

    const groupedNotes = computed(() => {
      const groups = {};
      filteredNotes.value.forEach(n => {
        const key = n.list_name || '_uncategorized';
        if (!groups[key]) groups[key] = [];
        groups[key].push(n);
      });
      return groups;
    });

    const groupKeys = computed(() => Object.keys(groupedNotes.value).sort());

    const currentNote = computed(() => {
      const m = route.value.match(/^\/repo\/(.+)/);
      if (!m) return null;
      return allNotes.value.find(n => n.slug === m[1]) || null;
    });

    // Todo list: all notes with todos, aggregated
    const allTodos = computed(() => {
      const todos = [];
      allNotes.value.forEach(n => {
        if (!n.todo_items || !n.todo_items.length) return;
        n.todo_items.forEach(t => {
          todos.push({ ...t, repo: n.repo_full_name, slug: n.slug });
        });
      });
      todos.sort((a, b) => (a.priority || 3) - (b.priority || 3));
      return todos;
    });

    // Relations: collect all relations into clusters
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

    // ── Markdown rendering helpers ──
    function renderMd(text) {
      if (!text) return '';
      const html = marked.parse(text, { breaks: true, gfm: true });
      return DOMPurify.sanitize(html);
    }

    function highlightBlocks() {
      nextTick(() => {
        document.querySelectorAll('.markdown-body pre code').forEach(block => {
          hljs.highlightElement(block);
        });
      });
    }

    // ── Colors ─────────────────────
    const langColors = {
      'Python': '#3572A5', 'JavaScript': '#F7DF1E', 'TypeScript': '#3178C6',
      'HTML': '#E34F26', 'CSS': '#563D7C', 'Go': '#00ADD8', 'Rust': '#DEA584',
      'Java': '#B07219', 'C': '#555555', 'C++': '#F34B7F', 'C#': '#178600',
      'Ruby': '#701516', 'PHP': '#4F5D95', 'Swift': '#F05138', 'Kotlin': '#A97BFF',
      'Scala': '#C22D40', 'Shell': '#89E051', 'Jupyter Notebook': '#DA5B0B',
      'Vue': '#4FC08D', 'Svelte': '#FF3E00', 'Dart': '#00B4AB',
    };
    function langColor(lang) { return langColors[lang] || '#8b949e'; }

    // ── Category presentation ───────
    const categoryIcons = {
      'tool': '🔧', 'lib': '📦', 'tutorial': '📖',
      'demo': '🎮', 'article': '📝', 'framework': '🏗️', 'other': '📁',
    };
    function catIcon(cat) { return categoryIcons[cat] || ''; }

    // ── Rating stars ────────────────
    function ratingStars(r) {
      if (!r || r < 1) return '';
      return '★'.repeat(r) + '☆'.repeat(5 - r);
    }

    // ── Maintenance indicators ──────
    const maintColor = {
      'active': 'var(--green)',
      'stale': 'var(--yellow)',
      'archived': 'var(--red)',
    };
    function maintStyle(m) { return { color: maintColor[m] || 'var(--text-muted)' }; }

    function toSlug(name) { return name.replace(/\//g, '.').toLowerCase(); }

    return {
      data, loading, error, route, searchQuery, filterLang, filterStatus,
      allNotes, stats, languages, filteredNotes, groupedNotes, groupKeys,
      currentNote, allTodos, allRelations,
      nav, renderMd, highlightBlocks, langColor, toSlug,
      catIcon, ratingStars, maintStyle,
    };
  },

  watch: {
    currentNote() { this.highlightBlocks(); },
  },
});

app.mount('#app');
