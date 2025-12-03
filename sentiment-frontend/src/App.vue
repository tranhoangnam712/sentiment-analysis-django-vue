<template>
  <div class="min-h-screen bg-gray-900 flex items-center justify-center p-6 text-gray-200">
    <div class="bg-gray-800 p-8 rounded-2xl shadow-xl w-full max-w-3xl border border-gray-700">

      <!-- Header -->
      <h1 class="text-3xl font-bold mb-6 text-center text-indigo-400 tracking-wide">
      Sentiment Analyzer
      </h1>

      <!-- Input Card -->
      <div class="bg-gray-900 p-5 rounded-xl shadow-sm border border-gray-700 mb-6">
        <textarea
          v-model="text"
          @input="onInput"
          class="w-full p-4 border rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none bg-gray-800 text-gray-200 transition"
          placeholder="Type something to analyze..."
          rows="3"
        ></textarea>
      </div>

      <!-- Result -->
      <div v-if="result" class="bg-gray-900 p-5 rounded-xl shadow-sm border border-gray-700 mb-6">
        <h2 class="text-xl font-bold mb-3 text-indigo-400">Result</h2>
        <p><strong>Text:</strong> {{ result.text }}</p>
        <p class="mt-2">
          <strong>Prediction:</strong>
          <span
            class="font-bold px-2 py-1 rounded-lg"
            :class="{
              'text-green-400 bg-green-900': result.prediction === 'Positive',
              'text-red-400 bg-red-900': result.prediction === 'Negative',
              'text-gray-300 bg-gray-800': result.prediction === 'Neutral'
            }"
          >
            {{ result.prediction }}
          </span>
        </p>
      </div>

      <!-- Error -->
      <p v-if="error" class="mt-3 text-red-400 font-medium text-center bg-red-900 p-3 rounded-lg">
        {{ error }}
      </p>

      <!-- History -->
      <h2 class="text-2xl font-bold mt-10 mb-4 text-indigo-400">History</h2>
      <div class="max-h-72 overflow-y-auto bg-gray-900 p-4 rounded-xl shadow-sm border border-gray-700 space-y-3">
        <div
          v-for="h in history"
          :key="h.id"
          class="p-3 rounded-lg border border-gray-700 hover:bg-gray-800 transition"
        >
          <p class="font-medium text-gray-200">{{ h.text }}</p>
          <p class="flex items-center gap-2 mt-1">
            <span
              class="font-bold px-2 py-0.5 rounded-lg text-sm"
              :class="{
                'text-green-400 bg-green-900': h.prediction === 'Positive',
                'text-red-400 bg-red-900': h.prediction === 'Negative',
                'text-gray-300 bg-gray-800': h.prediction === 'Neutral'
              }"
            >
              {{ h.prediction }}
            </span>
            <span class="text-xs text-gray-500">
              {{ formatDate(h.created_at) }}
            </span>
          </p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const text = ref('')
const result = ref(null)
const error = ref('')
const history = ref([])

let debounceTimer = null
const debounceDelay = 1000 // 1 second after typing stops

function formatDate(dt) {
  return new Date(dt).toLocaleString()
}

function onInput() {
  error.value = ''
  // Clear previous timer
  clearTimeout(debounceTimer)

  // Start a new timer
  debounceTimer = setTimeout(() => {
    analyze()
  }, debounceDelay)
}

async function analyze() {
  error.value = ''
  result.value = null

  if (!text.value.trim()) return

  try {
    const response = await fetch('http://127.0.0.1:8000/analyze/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text.value })
    })

    // Parse JSON only if content-type is JSON
    const contentType = response.headers.get("content-type")
    let data = {}
    if (contentType && contentType.includes("application/json")) {
      data = await response.json()
    }

    if (!response.ok) {
      // Backend returned error (400, 422, etc.)
      error.value = data.error || `Error ${response.status}`
    } else {
      result.value = data
      loadHistory()
    }

  } catch (e) {
    // This only triggers on network failure or invalid JSON
    error.value = 'Failed to connect to backend.'
    console.error(e)
  }
}


async function loadHistory() {
  try {
    const response = await fetch('http://127.0.0.1:8000/history/')
    history.value = await response.json()
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  loadHistory()
})
</script>
