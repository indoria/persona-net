(function() {
    'use strict';

    const DB_NAME = 'JSONEditorDB';
    const DB_VERSION = 1;
    const OBJECT_STORE_NAME = 'json_data';
    const LOCAL_STORAGE_PREFIX = 'json_editor_local_';
    const SESSION_STORAGE_PREFIX = 'json_editor_session_';
    const REST_API_BASE_URL = 'https://jsonplaceholder.typicode.com/posts';

    let indexedDBInstance;

    function openIndexedDB() {
        return new Promise((resolve, reject) => {
            if (indexedDBInstance) {
                resolve(indexedDBInstance);
                return;
            }

            const request = indexedDB.open(DB_NAME, DB_VERSION);

            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                if (!db.objectStoreNames.contains(OBJECT_STORE_NAME)) {
                    db.createObjectStore(OBJECT_STORE_NAME);
                }
            };

            request.onsuccess = (event) => {
                indexedDBInstance = event.target.result;
                resolve(indexedDBInstance);
            };

            request.onerror = (event) => {
                console.error('IndexedDB error:', event.target.error);
                reject(new Error(`IndexedDB error: ${event.target.error.message}`));
            };
        });
    }

    const LocalStorageAdapter = {
        store: async function(entity, data) {
            return new Promise((resolve) => {
                localStorage.setItem(LOCAL_STORAGE_PREFIX + entity, JSON.stringify(data));
                resolve();
            });
        },
        retrieve: async function(entity) {
            return new Promise((resolve) => {
                const data = localStorage.getItem(LOCAL_STORAGE_PREFIX + entity);
                resolve(data ? JSON.parse(data) : null);
            });
        },
        update: async function(entity, data) {
            return this.store(entity, data);
        },
        delete: async function(entity) {
            return new Promise((resolve) => {
                localStorage.removeItem(LOCAL_STORAGE_PREFIX + entity);
                resolve();
            });
        }
    };

    const SessionStorageAdapter = {
        store: async function(entity, data) {
            return new Promise((resolve) => {
                sessionStorage.setItem(SESSION_STORAGE_PREFIX + entity, JSON.stringify(data));
                resolve();
            });
        },
        retrieve: async function(entity) {
            return new Promise((resolve) => {
                const data = sessionStorage.getItem(SESSION_STORAGE_PREFIX + entity);
                resolve(data ? JSON.parse(data) : null);
            });
        },
        update: async function(entity, data) {
            return this.store(entity, data);
        },
        delete: async function(entity) {
            return new Promise((resolve) => {
                sessionStorage.removeItem(SESSION_STORAGE_PREFIX + entity);
                resolve();
            });
        }
    };

    const IndexedDBAdapter = {
        store: async function(entity, data) {
            const db = await openIndexedDB();
            return new Promise((resolve, reject) => {
                const transaction = db.transaction([OBJECT_STORE_NAME], 'readwrite');
                const store = transaction.objectStore(OBJECT_STORE_NAME);
                const request = store.put(data, entity);

                request.onsuccess = () => resolve();
                request.onerror = (event) => {
                    console.error('IndexedDB store error:', event.target.error);
                    reject(new Error(`IndexedDB store failed: ${event.target.error.message}`));
                };
            });
        },
        retrieve: async function(entity) {
            const db = await openIndexedDB();
            return new Promise((resolve, reject) => {
                const transaction = db.transaction([OBJECT_STORE_NAME], 'readonly');
                const store = transaction.objectStore(OBJECT_STORE_NAME);
                const request = store.get(entity);

                request.onsuccess = () => resolve(request.result || null);
                request.onerror = (event) => {
                    console.error('IndexedDB retrieve error:', event.target.error);
                    reject(new Error(`IndexedDB retrieve failed: ${event.target.error.message}`));
                };
            });
        },
        update: async function(entity, data) {
            return this.store(entity, data);
        },
        delete: async function(entity) {
            const db = await openIndexedDB();
            return new Promise((resolve, reject) => {
                const transaction = db.transaction([OBJECT_STORE_NAME], 'readwrite');
                const store = transaction.objectStore(OBJECT_STORE_NAME);
                const request = store.delete(entity);

                request.onsuccess = () => resolve();
                request.onerror = (event) => {
                    console.error('IndexedDB delete error:', event.target.error);
                    reject(new Error(`IndexedDB delete failed: ${event.target.error.message}`));
                };
            });
        }
    };

    const RestApiAdapter = {
        store: async function(entity, data) {
            const payload = { title: entity, body: JSON.stringify(data), userId: 1 };
            const response = await fetch(REST_API_BASE_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!response.ok) throw new Error(`REST API store failed: ${response.statusText}`);
            return await response.json();
        },
        retrieve: async function(entity) {
            const url = entity ? `${REST_API_BASE_URL}/${entity}` : REST_API_BASE_URL;
            const response = await fetch(url);
            if (!response.ok) {
                if (response.status === 404 && entity) return null;
                throw new Error(`REST API retrieve failed: ${response.statusText}`);
            }
            const data = await response.json();
            if (!entity && Array.isArray(data)) {
                return data.find(item => item.title === entity) || null;
            }
            return data;
        },
        update: async function(entity, data) {
            const payload = { title: entity, body: JSON.stringify(data), userId: 1 };
            const response = await fetch(`${REST_API_BASE_URL}/${entity}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!response.ok) throw new Error(`REST API update failed: ${response.statusText}`);
            return await response.json();
        },
        delete: async function(entity) {
            const response = await fetch(`${REST_API_BASE_URL}/${entity}`, {
                method: 'DELETE'
            });
            if (!response.ok) throw new Error(`REST API delete failed: ${response.statusText}`);
        }
    };

    window.StorageManager = {
        _adapters: {
            local: LocalStorageAdapter,
            session: SessionStorageAdapter,
            indexeddb: IndexedDBAdapter,
            restapi: RestApiAdapter
        },
        _currentAdapter: null,

        init: async function(defaultAdapterType = 'local') {
            this.setAdapter(defaultAdapterType);
            if (defaultAdapterType === 'indexeddb' || !indexedDBInstance) {
                try {
                    await openIndexedDB();
                    console.log('IndexedDB initialized.');
                } catch (error) {
                    console.error('Failed to initialize IndexedDB:', error);
                }
            }
        },

        setAdapter: function(adapterType) {
            if (!this._adapters[adapterType]) {
                throw new Error(`Invalid storage adapter type: ${adapterType}`);
            }
            this._currentAdapter = this._adapters[adapterType];
            console.log(`Storage adapter set to: ${adapterType}`);
        },

        getAdapter: function() {
            if (!this._currentAdapter) {
                throw new Error('No storage adapter has been set. Call StorageManager.init() first.');
            }
            return this._currentAdapter;
        },

        store: async function(entity, data) {
            return this.getAdapter().store(entity, data);
        },

        retrieve: async function(entity) {
            return this.getAdapter().retrieve(entity);
        },

        update: async function(entity, data) {
            return this.getAdapter().update(entity, data);
        },

        delete: async function(entity) {
            return this.getAdapter().delete(entity);
        }
    };
})();
