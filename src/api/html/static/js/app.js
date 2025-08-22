
(function() {
	// Helper: escape HTML
	function escapeHtml(unsafe) {
		if (!unsafe) return '';
		return String(unsafe)
			.replace(/&/g, '&amp;')
			.replace(/</g, '&lt;')
			.replace(/>/g, '&gt;')
			.replace(/"/g, '&quot;')
			.replace(/'/g, '&#039;');
	}

	// Build query URL from form
	function buildQueryUrl() {
		const formData = new FormData(document.getElementById('filtersForm'));
		const params = new URLSearchParams();
		
		// Handle topics (can be multiple checkboxes with the same name)
		const topics = formData.getAll('topics');
		topics.forEach(topic => {
			if (topic) params.append('topics', topic);
		});
		
		// Handle limit parameter (max articles)
		const maxArticles = document.getElementById('maxArticles').value;
		if (maxArticles) params.append('limit', maxArticles);
		
		// Handle date parameters (only add if they have values)
		const fromDate = document.getElementById('fromDate').value;
		if (fromDate) params.append('from_date', new Date(fromDate).toISOString());
		
		const toDate = document.getElementById('toDate').value;
		if (toDate) params.append('to_date', new Date(toDate).toISOString());
		
		// Handle sort order
		const orderBy = document.getElementById('orderBy').value;
		if (orderBy === 'match') params.append('sort_by_match', 'true');
		
		return `/api/get_news_by_topic?${params.toString()}`;
	}

	// Show loading spinner
	function showLoading() {
		$('#resultsContainer').html('<div class="text-center"><div class="spinner-border" role="status"></div></div>');
	}

	// Render a single article card
	function renderArticle(a) {
		const title = a.title || 'Untitled';
		const url = a.url || '#';
		const source = a.source || '';
		const author = a.author || '';
		const desc = a.description || '';
		const contentHead = a.content_snippet || '';
		const published = a.published_at ? new Date(a.published_at) : null;
		const topics = Array.isArray(a.topics) ? a.topics : [];
		const dateStr = published ? published.toLocaleString() : '';
		let hostname = '';
		try { hostname = new URL(url, window.location.origin).hostname; } catch (_e) {}

		const $card = $('<div class="card mb-3 p-3"></div>');
		const $title = $('<div class="article-title"></div>').text(title);
		const $meta = $(
			`<div class="meta mb-2">
				<span class="me-2">Source: </span>
				<a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(source || hostname)}</a>
				${author ? ` &middot; <span class="ms-2">Author: ${escapeHtml(author)}</span>` : ''}
				${dateStr ? ` &middot; <span class="ms-2">${escapeHtml(dateStr)}</span>` : ''}
			</div>`
		);
		const $desc = $('<div class="mb-2"/>').text(desc);
		const $content = $('<div class="mb-2"/>').text(contentHead);
		const $more = $('<a class="link-primary" target="_blank" rel="noopener noreferrer">continue reading…</a>').attr('href', url);
		const topicsStr = topics.map(t => escapeHtml(t)).join(', ');
		const $topics = $(`<div class="topics"><strong>Topics:</strong> ${topicsStr}</div>`);
		$card.append($title, $meta, $desc, $content, $more, $topics);
		$('#resultsContainer').append($card);
	}

	// Fetch and render articles
	async function fetchAndRender(url) {
		showLoading();
		try {
			const response = await fetch(url);
			if (!response.ok) throw new Error('Network error');
			const data = await response.json();
			$('#resultsContainer').empty();
			if (!Array.isArray(data) || !data.length) {
				$('#resultsContainer').html('<div class="alert alert-info">No results found.</div>');
				return;
			}
			data.forEach(renderArticle);
		} catch (error) {
			console.error('Error fetching data:', error);
			$('#resultsContainer').html('<div class="alert alert-danger">Error fetching data. Please try again.</div>');
		}
	}

	// Load topics for filter dropdown
	async function loadTopics() {
		try {
			const response = await fetch('/api/get_topics');
			if (!response.ok) throw new Error('Network error');
			const topics = await response.json();
			const $topicsContainer = $('#topicsContainer');
			$topicsContainer.empty();
			topics.forEach(topic => {
				const checkboxId = `topic-${topic.replace(/\s+/g, '-')}`;
				$topicsContainer.append(`
					<div class="form-check">
						<input class="form-check-input" type="checkbox" name="topics" value="${topic}" id="${checkboxId}">
						<label class="form-check-label" for="${checkboxId}">${topic}</label>
					</div>
				`);
			});
			$('#topicsLoading').hide();
		} catch (error) {
			console.error('Error loading topics:', error);
			$('#topicsLoading').text('Error loading topics');
		}
	}

	// Form submit handler
	$('#filtersForm').on('submit', function(e) {
		e.preventDefault();
		const url = buildQueryUrl();
		fetchAndRender(url);
	});

	// Initializations
	$(async function() {
		// Initialize slider value display
		$('#maxArticlesValue').text($('#maxArticles').val());
		
		// Set up slider change event
		$('#maxArticles').on('input', function() {
			$('#maxArticlesValue').text($(this).val());
		});
		
		// Load topics and initial articles
		await loadTopics();
		fetchAndRender('/api/get_news_by_topic?limit=10');
	});
})();