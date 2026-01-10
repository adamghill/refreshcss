import pytest

from refreshcss.html.file import File


@pytest.fixture
def complex_html():
    """A realistic Django template repeated to make it larger."""
    return (
        """
    <div class="container {% if active %}active{% endif %}">
        <header class="header">
            <h1 id="title">{{ page_title }}</h1>
            <nav class="navbar navbar-expand-lg">
                <ul class="nav">
                    {% for item in menu_items %}
                        <li class="nav-item {% if item.active %}active{% endif %}">
                            <a href="{{ item.url }}" class="nav-link">{{ item.name }}</a>
                        </li>
                    {% endfor %}
                </ul>
            </nav>
        </header>

        <main class="content">
            <div class="row">
                <div class="col-md-8">
                    <article class="post">
                        <h2 class="post-title">{{ post.title }}</h2>
                        <div class="post-meta">
                            <span class="author">{{ post.author }}</span>
                            <span class="date">{{ post.date }}</span>
                        </div>
                        <div class="post-content">
                            {{ post.content }}
                        </div>
                    </article>
                </div>
        
                <aside class="col-md-4 sidebar">
                    <div class="widget">
                        <h3 class="widget-title">Recent Posts</h3>
                        <ul class="widget-list">
                            {% for post in recent_posts %}
                                <li class="widget-item">
                                    <a href="{{ post.url }}">{{ post.title }}</a>
                                </li>
                            {% endfor %}
                        </ul>
                    </div>
                </aside>
            </div>
        </main>

        <footer class="footer">
            <p class="copyright">&copy; 2026 My Site</p>
        </footer>
    </div>
    """
        * 10
    )


def test_html_file_classes_performance(complex_html, benchmark):
    """Benchmark HTML class extraction performance."""
    file = File(None)
    file.text = complex_html

    benchmark(lambda: file.classes)


def test_html_file_ids_performance(complex_html, benchmark):
    """Benchmark HTML ID extraction performance."""
    file = File(None)
    file.text = complex_html

    benchmark(lambda: file.ids)


def test_html_file_elements_performance(complex_html, benchmark):
    """Benchmark HTML element extraction performance."""
    file = File(None)
    file.text = complex_html

    benchmark(lambda: file.elements)
