'use strict';

const FASTAPI_URL = 'http://127.0.0.1:8080';

document.addEventListener('DOMContentLoaded', () => {
  const searchForm = document.getElementById('search-form');
  const searchInput = document.getElementById('search-input');
  const searchList = document.getElementById('search-list');

  // 検索ボタン
  searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const searchText = searchInput.value.trim();
    if (searchText !== '') {
      search(searchText).then((results) => {
        while(searchList.firstChild){
          searchList.removeChild(searchList.firstChild)
        }
        for (const result of results) {
          addSearchItem(result._source.title, result._source.author);
        }
      });
    }
  });

  class SearchItem {
    constructor(title, author) {
      this.title = title;
      this.author = author;
    }

    render() {
      const li = document.createElement('li');

      const span = document.createElement('span');
      span.textContent = this.title;

      const p = document.createElement('p');
      p.textContent = this.author;

      li.appendChild(span);
      li.appendChild(p);
      searchList.appendChild(li);
    }
  }

  function addSearchItem(title, author) {
    const searchItem = new SearchItem(title, author);
    searchItem.render();
  }
});

async function search(q) {
  try {
    const response = await fetch(`${FASTAPI_URL}/search?q=${q}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`検索に失敗しました: ${response.status}`);
    }

    const results = await response.json();
    return results;
  } catch (e) {
    console.error('エラーが発生しました: ', e);
  }
}