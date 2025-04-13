<template>
  <div
    class="min-h-screen bg-gradient-to-br from-gray-50 via-gray-100 to-indigo-50 dark:from-gray-800 dark:via-gray-900 dark:to-black p-4 sm:p-6 lg:p-8 font-inter text-gray-800 dark:text-gray-200"
  >
    <div class="max-w-7xl mx-auto">
      <header
        class="mb-8 flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0"
      >
        <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <div class="flex items-center space-x-3">
          <button
            @click="openAddAccountModal"
            title="Add New Account"
            class="p-2 bg-indigo-600 text-white rounded-full shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition duration-300 ease-in-out"
          >
            <PlusIcon class="h-5 w-5" aria-hidden="true" />
          </button>
          <button
            @click="openAddTransactionModal"
            title="Add New Transaction (Quick Add)"
            class="p-2 bg-green-600 text-white rounded-full shadow-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition duration-300 ease-in-out"
          >
            <ChatBubbleLeftEllipsisIcon class="h-5 w-5" aria-hidden="true" />
          </button>
          <button
            @click="handleLogout"
            title="Logout"
            class="p-2 bg-red-600 text-white rounded-full shadow-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition duration-300 ease-in-out"
          >
            <ArrowRightOnRectangleIcon class="h-5 w-5" aria-hidden="true" />
          </button>
        </div>
      </header>

      <div
        v-if="dataStore.isLoading && initialLoad"
        class="text-center py-10 text-gray-600 dark:text-gray-400"
      >
        <svg
          class="animate-spin h-8 w-8 text-indigo-600 dark:text-indigo-400 mx-auto mb-3"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          ></circle>
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
        Loading dashboard data...
      </div>
      <div
        v-else-if="dataStore.error && !showAddAccountModal && !showAddTransactionModal"
        class="p-4 mb-6 bg-red-100 dark:bg-red-900 border border-red-300 dark:border-red-700 rounded-lg shadow text-sm text-red-700 dark:text-red-200 flex items-center space-x-2"
      >
        <ExclamationTriangleIcon class="h-5 w-5 flex-shrink-0" aria-hidden="true" />
        <span>{{ dataStore.error }}</span>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 space-y-6">
          <section
            class="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden transition-all duration-300 ease-in-out"
          >
            <div class="p-5 border-b border-gray-200 dark:border-gray-700">
              <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200">Your Accounts</h2>
            </div>
            <div class="p-5">
              <div
                v-if="dataStore.accounts.length > 0"
                class="grid grid-cols-1 md:grid-cols-2 gap-4"
              >
                <div
                  v-for="account in dataStore.accounts"
                  :key="account.id"
                  class="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:shadow-lg hover:scale-[1.02] transition-all duration-200 ease-in-out bg-gray-50 dark:bg-gray-700/50"
                >
                  <div class="flex justify-between items-center mb-1">
                    <span class="font-medium text-gray-900 dark:text-white truncate">{{
                      account.name
                    }}</span>
                    <BanknotesIcon
                      class="h-5 w-5 text-indigo-500 dark:text-indigo-400 flex-shrink-0 ml-2"
                    />
                  </div>
                  <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">{{ account.type }}</p>
                  <p class="text-lg font-semibold text-gray-900 dark:text-white">
                    {{ formatCurrency(account.balance, account.currency_code) }}
                  </p>
                </div>
              </div>
              <p v-else class="text-center text-gray-500 dark:text-gray-400 py-4">
                No accounts found. Click the '+' button above to add one!
              </p>
            </div>
          </section>

          <section
            class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-5 transition-all duration-300 ease-in-out"
          >
            <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-4">
              Spending & Income (Last 7 Days)
            </h2>
            <div
              v-if="dataStore.isLoadingChart"
              class="text-center py-10 text-gray-500 dark:text-gray-400"
            >
              Loading chart data...
            </div>
            <div v-else-if="chartDataReady" class="h-64 sm:h-72">
              <Line :data="chartData" :options="chartOptions" />
            </div>
            <p v-else class="text-center text-gray-500 dark:text-gray-400 py-10">
              Not enough transaction data for chart.
            </p>
          </section>
        </div>

        <div class="lg:col-span-1">
          <section
            class="bg-white dark:bg-gray-800 rounded-lg shadow-lg h-full flex flex-col transition-all duration-300 ease-in-out"
          >
            <div class="p-5 border-b border-gray-200 dark:border-gray-700">
              <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200">
                Recent Transactions
              </h2>
            </div>
            <div
              v-if="sortedTransactions.length > 0"
              class="flex-grow overflow-y-auto p-5 space-y-3 max-h-[calc(100vh-16rem)] custom-scrollbar"
            >
              <div
                v-for="tx in sortedTransactions"
                :key="tx.id"
                class="flex justify-between items-center p-3 border-b border-gray-100 dark:border-gray-700/50 last:border-b-0 hover:bg-gray-50 dark:hover:bg-gray-700/30 rounded transition-colors duration-150"
              >
                <div>
                  <p class="font-medium text-gray-900 dark:text-white text-sm">
                    {{ tx.description }}
                  </p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">
                    {{ formatDate(tx.transaction_date) }} - {{ tx.category || 'Uncategorized' }}
                  </p>
                </div>
                <span
                  :class="[
                    tx.type === 'INCOME'
                      ? 'text-green-600 dark:text-green-400'
                      : 'text-red-600 dark:text-red-400',
                    'font-semibold text-sm flex-shrink-0 ml-2',
                  ]"
                >
                  {{ formatCurrency(tx.amount, tx.currency_code) }}
                </span>
              </div>
            </div>
            <p v-else class="text-center text-gray-500 dark:text-gray-400 py-10 px-5">
              No recent transactions found.
            </p>
          </section>
        </div>
      </div>
    </div>

    <Transition name="modal">
      <div
        v-if="showAddAccountModal"
        class="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-60 flex items-center justify-center p-4"
      >
        <div
          class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6 space-y-4 transform transition-all duration-300 ease-out"
        >
          <div class="flex justify-between items-center">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">Add New Account</h3>
            <button
              @click="closeAddAccountModal"
              class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <XMarkIcon class="h-6 w-6" />
            </button>
          </div>
          <form @submit.prevent="handleAddAccountSubmit" class="space-y-4">
            <div>
              <label
                for="accName"
                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >Account Name</label
              >
              <input
                v-model="newAccount.name"
                type="text"
                id="accName"
                required
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
                placeholder="e.g., Main Checking"
              />
            </div>
            <div>
              <label
                for="accType"
                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >Account Type</label
              >
              <select
                v-model="newAccount.type"
                id="accType"
                required
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
              >
                <option disabled value="">Select type</option>
                <option>Checking</option>
                <option>Savings</option>
                <option>Credit Card</option>
                <option>Cash</option>
                <option>Investment</option>
                <option>Loan</option>
                <option>Other</option>
              </select>
            </div>
            <div>
              <label
                for="accBalance"
                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >Initial Balance (Optional)</label
              >
              <input
                v-model.number="newAccount.balance"
                type="number"
                step="0.01"
                id="accBalance"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
                placeholder="0.00"
              />
            </div>
            <div>
              <label
                for="accCurrency"
                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >Currency Code (e.g., INR, USD)</label
              >
              <input
                v-model="newAccount.currency_code"
                type="text"
                id="accCurrency"
                maxlength="3"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out uppercase text-sm"
                placeholder="INR"
              />
            </div>
            <p v-if="modalError" class="text-sm text-red-600 dark:text-red-400">{{ modalError }}</p>
            <div class="flex justify-end space-x-3 pt-2">
              <button
                type="button"
                @click="closeAddAccountModal"
                class="inline-flex justify-center py-2 px-4 border border-gray-300 dark:border-gray-600 shadow-sm text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="dataStore.isLoading"
                class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out disabled:opacity-50"
              >
                <span v-if="!dataStore.isLoading">Add Account</span> <span v-else>Adding...</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>

    <Transition name="modal">
      <div
        v-if="showAddTransactionModal"
        class="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-60 flex items-center justify-center p-4"
      >
        <div
          class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full transform transition-all duration-300 ease-out"
        >
          <div
            class="flex justify-between items-center p-4 sm:p-6 border-b border-gray-200 dark:border-gray-700"
          >
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">
              {{
                dataStore.parsedTransactions.length > 0
                  ? 'Confirm Transactions'
                  : 'Add Transaction (Quick Add)'
              }}
            </h3>
            <button
              @click="closeAddTransactionModal"
              class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <XMarkIcon class="h-6 w-6" />
            </button>
          </div>

          <div class="p-4 sm:p-6 space-y-4 max-h-[70vh] overflow-y-auto custom-scrollbar">
            <form
              v-if="dataStore.parsedTransactions.length === 0"
              @submit.prevent="handleNlpSubmit"
              class="space-y-4"
            >
              <div>
                <label
                  for="nlpText"
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                  >Describe your transaction(s)</label
                >
                <textarea
                  v-model="nlpInputText"
                  id="nlpText"
                  rows="3"
                  required
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
                  placeholder="e.g., ₹1500 groceries yesterday, ₹200 coffee today from HDFC card"
                ></textarea>
              </div>
              <p v-if="modalError" class="text-sm text-red-600 dark:text-red-400">
                {{ modalError }}
              </p>
              <div class="flex justify-end space-x-3 pt-2">
                <button
                  type="button"
                  @click="closeAddTransactionModal"
                  class="inline-flex justify-center py-2 px-4 border border-gray-300 dark:border-gray-600 shadow-sm text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  :disabled="dataStore.isLoadingParse"
                  class="inline-flex justify-center items-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out disabled:opacity-50"
                >
                  <svg
                    v-if="dataStore.isLoadingParse"
                    class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      class="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      stroke-width="4"
                    ></circle>
                    <path
                      class="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  <span>{{ dataStore.isLoadingParse ? 'Parsing...' : 'Parse Transaction' }}</span>
                </button>
              </div>
            </form>

            <div v-else class="space-y-4">
              <p class="text-sm text-gray-600 dark:text-gray-400">
                Review and confirm the transactions found. You can edit details before saving.
              </p>
              <p v-if="modalError" class="text-sm text-red-600 dark:text-red-400">
                {{ modalError }}
              </p>

              <div
                v-for="(tx, index) in dataStore.parsedTransactions"
                :key="tx.tempId || index"
                class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 space-y-3 bg-gray-50 dark:bg-gray-800/50 relative"
              >
                <div
                  v-if="tx.isSaving"
                  class="absolute inset-0 bg-white/70 dark:bg-gray-900/70 flex items-center justify-center rounded-lg z-10"
                >
                  <svg
                    class="animate-spin h-6 w-6 text-indigo-600 dark:text-indigo-400"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      class="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      stroke-width="4"
                    ></circle>
                    <path
                      class="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                </div>
                <p v-if="tx.saveError" class="text-xs text-red-600 dark:text-red-400 mb-2">
                  {{ tx.saveError }}
                </p>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label
                      :for="'txDesc-' + index"
                      class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1"
                      >Description</label
                    >
                    <input
                      v-model="tx.description"
                      type="text"
                      :id="'txDesc-' + index"
                      required
                      class="block w-full px-2 py-1 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
                    />
                  </div>
                  <div>
                    <label
                      :for="'txCategory-' + index"
                      class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1"
                      >Category</label
                    >
                    <input
                      v-model="tx.category"
                      type="text"
                      :id="'txCategory-' + index"
                      class="block w-full px-2 py-1 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
                      placeholder="Optional"
                    />
                  </div>
                </div>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div>
                    <label
                      :for="'txAmount-' + index"
                      class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1"
                      >Amount</label
                    >
                    <input
                      v-model.number="tx.amount"
                      type="number"
                      step="0.01"
                      :id="'txAmount-' + index"
                      required
                      class="block w-full px-2 py-1 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
                    />
                  </div>
                  <div>
                    <label
                      :for="'txType-' + index"
                      class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1"
                      >Type</label
                    >
                    <select
                      v-model="tx.type"
                      :id="'txType-' + index"
                      required
                      class="block w-full px-2 py-1 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
                    >
                      <option>EXPENSE</option>
                      <option>INCOME</option>
                    </select>
                  </div>
                  <div>
                    <label
                      :for="'txDate-' + index"
                      class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1"
                      >Date</label
                    >
                    <input
                      v-model="tx.date"
                      type="date"
                      :id="'txDate-' + index"
                      required
                      class="block w-full px-2 py-1 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
                    />
                  </div>
                  <div>
                    <label
                      :for="'txAccount-' + index"
                      class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1"
                      >Account</label
                    >
                    <select
                      v-model="tx.account_id"
                      :id="'txAccount-' + index"
                      required
                      class="block w-full px-2 py-1 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
                    >
                      <option disabled value="">Select</option>
                      <option v-for="acc in dataStore.accounts" :key="acc.id" :value="acc.id">
                        {{ acc.name }}
                      </option>
                    </select>
                  </div>
                </div>

                <div class="flex justify-end space-x-2 pt-2">
                  <button
                    @click="discardParsedTransaction(index)"
                    type="button"
                    title="Discard this transaction"
                    class="p-1.5 text-gray-500 hover:text-red-600 dark:text-gray-400 dark:hover:text-red-500 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-1 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out"
                  >
                    <XMarkIcon class="h-5 w-5" />
                  </button>
                  <button
                    @click="confirmParsedTransaction(index)"
                    type="button"
                    title="Confirm and save this transaction"
                    class="p-1.5 text-gray-500 hover:text-green-600 dark:text-gray-400 dark:hover:text-green-500 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-1 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out"
                  >
                    <CheckIcon class="h-5 w-5" />
                  </button>
                </div>
              </div>

              <div class="flex justify-end pt-4">
                <button
                  type="button"
                  @click="closeAddTransactionModal"
                  class="inline-flex justify-center py-2 px-4 border border-gray-300 dark:border-gray-600 shadow-sm text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out"
                >
                  {{ dataStore.parsedTransactions.length > 0 ? 'Done' : 'Cancel' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, reactive, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useDataStore } from '@/stores/dataStore'
import { apiClient } from '@/stores/authStore'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler,
} from 'chart.js'
import {
  BanknotesIcon,
  ArrowRightOnRectangleIcon,
  ExclamationTriangleIcon,
  PlusIcon,
  ChatBubbleLeftEllipsisIcon,
  XMarkIcon,
  CheckIcon,
} from '@heroicons/vue/24/outline'
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import relativeTime from 'dayjs/plugin/relativeTime'
import customParseFormat from 'dayjs/plugin/customParseFormat'

dayjs.extend(utc)
dayjs.extend(relativeTime)
dayjs.extend(customParseFormat)

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler,
)

const router = useRouter()
const authStore = useAuthStore()
const dataStore = useDataStore()

const initialLoad = ref(true)
const showAddAccountModal = ref(false)
const showAddTransactionModal = ref(false)
const nlpInputText = ref('')
const modalError = ref('')

const newAccount = reactive({
  name: '',
  type: '',
  balance: 0,
  currency_code: 'INR',
})

const sortedTransactions = computed(() => {
  return [...dataStore.recentTransactions]
    .filter((tx) => tx && tx.date)
    .sort((a, b) => dayjs(b.date).valueOf() - dayjs(a.date).valueOf())
})

const chartData = computed(() => {
  const labels = []
  const incomeData = []
  const expenseData = []
  const daysMap = new Map()

  for (let i = 6; i >= 0; i--) {
    const date = dayjs().subtract(i, 'day')
    const formattedDate = date.format('YYYY-MM-DD')
    const label = date.format('ddd')
    labels.push(label)
    daysMap.set(formattedDate, { income: 0, expense: 0 })
  }

  dataStore.chartTransactions.forEach((tx) => {
    const date = dayjs(tx.transaction_date).format('YYYY-MM-DD')
    if (daysMap.has(date)) {
      const dayTotal = daysMap.get(date)
      if (tx.type === 'INCOME') {
        dayTotal.income += tx.amount
      } else if (tx.type === 'EXPENSE') {
        dayTotal.expense += tx.amount
      }
    }
  })

  daysMap.forEach((totals) => {
    incomeData.push(totals.income)
    expenseData.push(totals.expense)
  })

  return {
    labels,
    datasets: [
      {
        label: 'Income',
        backgroundColor: 'rgba(16, 185, 129, 0.2)',
        borderColor: 'rgb(16, 185, 129)',
        data: incomeData,
        tension: 0.3,
        fill: true,
      },
      {
        label: 'Expense',
        backgroundColor: 'rgba(239, 68, 68, 0.2)',
        borderColor: 'rgb(239, 68, 68)',
        data: expenseData,
        tension: 0.3,
        fill: true,
      },
    ],
  }
})

const chartDataReady = computed(() => {
  return dataStore.chartTransactions.length > 0
})

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
      labels: {
        color: document.documentElement.classList.contains('dark') ? '#e5e7eb' : '#4b5563',
        font: {
          family: 'Inter, sans-serif',
        },
      },
    },
    tooltip: {
      mode: 'index',
      intersect: false,
      backgroundColor: document.documentElement.classList.contains('dark')
        ? 'rgba(31, 41, 55, 0.9)'
        : 'rgba(255, 255, 255, 0.9)', // Dark/light tooltip bg
      titleColor: document.documentElement.classList.contains('dark') ? '#f3f4f6' : '#1f2937',
      bodyColor: document.documentElement.classList.contains('dark') ? '#d1d5db' : '#374151',
      borderColor: document.documentElement.classList.contains('dark') ? '#4b5563' : '#e5e7eb',
      borderWidth: 1,
      padding: 10,
      callbacks: {
        label: function (context) {
          let label = context.dataset.label || ''
          if (label) {
            label += ': '
          }
          if (context.parsed.y !== null) {
            // Use the formatting function
            label += formatCurrency(context.parsed.y, dataStore.accounts[0]?.currency_code || 'INR')
          }
          return label
        },
      },
    },
  },
  scales: {
    x: {
      grid: {
        display: false, // Hide x-axis grid lines
      },
      ticks: {
        color: document.documentElement.classList.contains('dark') ? '#9ca3af' : '#6b7280', // Dark/light axis ticks
        font: { family: 'Inter, sans-serif' },
      },
      border: {
        color: document.documentElement.classList.contains('dark') ? '#4b5563' : '#e5e7eb', // Axis line color
      },
    },
    y: {
      grid: {
        color: document.documentElement.classList.contains('dark') ? '#374151' : '#e5e7eb', // Dark/light y-axis grid lines
        drawBorder: false,
      },
      ticks: {
        color: document.documentElement.classList.contains('dark') ? '#9ca3af' : '#6b7280',
        font: { family: 'Inter, sans-serif' },
        callback: function (value) {
          // Format Y-axis labels as currency
          return formatCurrency(value, dataStore.accounts[0]?.currency_code || 'INR', true) // Add a flag for compact formatting
        },
      },
      border: {
        display: false, // Hide Y axis line itself
      },
    },
  },
}))

const formatCurrency = (value, currencyCode = 'INR', compact = false) => {
  if (value === null || value === undefined) return ''
  const options = {
    style: 'currency',
    currency: currencyCode || 'INR', // Default to INR if not provided
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }
  if (compact) {
    options.notation = 'compact'
    options.minimumFractionDigits = 0 // Less precision needed for compact axis labels
    options.maximumFractionDigits = 1
  }
  try {
    return new Intl.NumberFormat('en-IN', options).format(value) // Use en-IN for Indian Rupee formatting
  } catch (e) {
    // Fallback for invalid currency code or other errors
    console.warn('Currency formatting failed:', e)
    options.currency = 'INR' // Fallback to INR
    return new Intl.NumberFormat('en-IN', options).format(value)
  }
}

// Format date (e.g., Apr 13, 2025)
const formatDate = (dateString) => {
  if (!dateString) return ''
  return dayjs(dateString).format('MMM D, YYYY')
}

// Format date for input type="date" (YYYY-MM-DD)
const formatDateForInput = (dateString) => {
  if (!dateString) return dayjs().format('YYYY-MM-DD') // Default to today if no date
  // Try parsing common formats, default to ISO if it fails
  const parsedDate = dayjs(dateString, ['YYYY-MM-DDTHH:mm:ssZ', 'YYYY-MM-DD', dayjs.ISO_8601], true)
  return parsedDate.isValid() ? parsedDate.format('YYYY-MM-DD') : dayjs().format('YYYY-MM-DD')
}

// Convert YYYY-MM-DD back to ISO string for backend
const formatInputDateToISO = (dateString) => {
  if (!dateString) return dayjs().toISOString() // Default to now if invalid
  return dayjs.utc(dateString).hour(12).toISOString()
}

// Add Account Modal Logic
const openAddAccountModal = () => {
  modalError.value = ''
  // Reset form
  Object.assign(newAccount, { name: '', type: '', balance: 0, currency_code: 'INR' })
  showAddAccountModal.value = true
}
const closeAddAccountModal = () => {
  showAddAccountModal.value = false
}
const handleAddAccountSubmit = async () => {
  modalError.value = ''
  // Basic validation
  if (!newAccount.name || !newAccount.type) {
    modalError.value = 'Account name and type are required.'
    return
  }
  // Ensure balance is a number
  newAccount.balance = Number(newAccount.balance) || 0
  // Uppercase currency code
  newAccount.currency_code = (newAccount.currency_code || 'INR').toUpperCase()

  const success = await dataStore.addAccount(newAccount) // Call Pinia store action
  if (success) {
    closeAddAccountModal()
  } else {
    modalError.value = dataStore.error || 'Failed to add account. Please try again.'
  }
}

// Add Transaction Modal Logic
const openAddTransactionModal = () => {
  modalError.value = ''
  nlpInputText.value = ''
  dataStore.clearParsedTransactions() // Clear previous results from store
  showAddTransactionModal.value = true
}
const closeAddTransactionModal = () => {
  showAddTransactionModal.value = false
  // Important: Clear parsed transactions when closing the modal fully
  dataStore.clearParsedTransactions()
  modalError.value = '' // Clear modal error on close
}

// Handle NLP text submission
const handleNlpSubmit = async () => {
  modalError.value = ''
  if (!nlpInputText.value.trim()) {
    modalError.value = 'Please describe the transaction(s).'
    return
  }

  const success = await dataStore.parseTransactionsNLP(nlpInputText.value)

  if (!success) {
    modalError.value =
      dataStore.error ||
      'Could not parse transactions. Please check the format or try adding manually.'
  }
}

const discardParsedTransaction = (index) => {
  dataStore.removeParsedTransaction(index)
  if (dataStore.parsedTransactions.length === 0) {
    closeAddTransactionModal()
  }
}

const confirmParsedTransaction = async (index) => {
  const transaction = dataStore.parsedTransactions[index]

  dataStore.setParsedTransactionStatus(index, { saveError: null })

  if (!transaction.account_id) {
    dataStore.setParsedTransactionStatus(index, { saveError: 'Please select an account.' })
    return
  }
  if (!transaction.amount || isNaN(transaction.amount) || transaction.amount <= 0) {
    dataStore.setParsedTransactionStatus(index, {
      saveError: 'Please enter a valid positive amount.',
    })
    return
  }
  if (!transaction.description) {
    dataStore.setParsedTransactionStatus(index, { saveError: 'Description cannot be empty.' })
    return
  }
  if (!transaction.date) {
    dataStore.setParsedTransactionStatus(index, { saveError: 'Please select a valid date.' })
    return
  }

  const transactionData = {
    account_id: transaction.account_id,
    amount: transaction.amount,
    type: transaction.type,
    category: transaction.category || null,
    description: transaction.description,
    date: formatInputDateToISO(transaction.date),
  }

  dataStore.setParsedTransactionStatus(index, { isSaving: true })

  const success = await dataStore.createTransaction(transactionData)

  if (success) {
    dataStore.removeParsedTransaction(index)
    if (dataStore.parsedTransactions.length === 0) {
      closeAddTransactionModal()
    }
  } else {
    dataStore.setParsedTransactionStatus(index, {
      isSaving: false,
      saveError: dataStore.error || 'Failed to save transaction.',
    })
  }
}

// Handle user logout
const handleLogout = () => {
  authStore.logout()
  router.push('/login') // Redirect to login page after logout
}

onMounted(async () => {
  await dataStore.fetchInitialData()
  initialLoad.value = false
})

// Watch for changes in parsed transactions to format dates for input
watch(
  () => dataStore.parsedTransactions,
  (newTransactions) => {
    if (newTransactions) {
      newTransactions.forEach((tx, index) => {
        // Add the formatted date property if it doesn't exist
        if (!tx.hasOwnProperty('date')) {
          dataStore.setParsedTransactionDateFormatted(
            index,
            formatDateForInput(tx.transaction_date),
          )
        }
        // Add other properties needed for UI state if they don't exist
        if (!tx.hasOwnProperty('isSaving')) {
          dataStore.setParsedTransactionStatus(index, { isSaving: false })
        }
        if (!tx.hasOwnProperty('saveError')) {
          dataStore.setParsedTransactionStatus(index, { saveError: null })
        }
      })
    }
  },
  { deep: true, immediate: true },
)
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
}
.modal-enter-to,
.modal-leave-from {
  opacity: 1;
  transform: scale(1) translateY(0);
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #d1d5db; 
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #4b5563;
}
.dark .custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}
</style>
