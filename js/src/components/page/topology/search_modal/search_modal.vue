<template>
  <div id="search-modal">
    <div class="modal-background" @click="hideModal"></div>
    <div class="modal-content">
      <div class="modal-title">
        Search
      </div>

      <div class="search-type-area margin-top-16">
        <div class="input-group vertical">
          <label for="mode">Search Type</label>
          <select class='search-type-selector padding-left-8' v-model='search_type'>
            <option v-for='(type, index) in search_types'
              :key='index' :value='type'>{{ type }}</option>
          </select>
        </div>
      </div>

      <div class="modal-param-area margin-top-16">
        <div v-for="(condition, i) in search_conditions" :key="i"
          class="condition-row">
          <div class='input-group margin-right-8'>
            <select class='data-type padding-left-8' v-model='condition["data_type"]'>
              <option v-for='(type, index) in data_types'
                :key='index' :value='type'>{{ type }}</option>
            </select>
          </div>

          <div class='input-group margin-right-8'>
            <select class='data-type padding-left-8' v-model='condition["column"]'>
              <option v-for='(col, index) in columns[condition["data_type"]]'
                :key='index' :value='index'>{{ col }}</option>
            </select>
          </div>

          <div class='input-group margin-right-8'>
            <select class='operator padding-left-8' v-model='condition["operator"]'>
              <option v-for='(op, index) in operators[condition["data_type"]]'
                :key='index' :value='op'>{{ op }}</option>
            </select>
          </div>

          <input v-if='condition["data_type"]==="number"' type="number" step="0.01"
            class="search-value"
            v-model='condition["value"]' />
          <input v-if='condition["data_type"]==="text"' type="text"
            class="search-value"
            v-model='condition["value"]' />

          <button class="remove-button margin-left-8"
            @click="removeCondition(i)">
            <i class="fa fa-minus" aria-hidden="true"></i>
          </button>
        </div>

        <button class="add-button margin-top-8" @click="addCondition()">
          <i class="fa fa-plus" aria-hidden="true"></i>
        </button>
      </div>

      <div class="modal-button-area margin-top-16">
        <button class="search-button" @click="search">
          <i class="fa fa-search" aria-hidden="true"></i> Search
        </button>

        <button class="cancel-button" @click="hideModal">
          CANCEL
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchModal",
  data: function() {
    return {
      data_types: ["number", "text"],
      operators: {
        "number": ["=", ">", "<"],
        "text": ["=", "like"]
      },
      search_types: ["and", "or"],
      search_conditions: this.$store.state.search_conditions,
    }
  },
  computed: {
    search_type: {
      get: function() {
        return this.$store.state.search_type;
      },
      set: function(val) {
        this.$store.commit('set_search_type', {
          'val': val,
        });
      },
    },
    columns: function() {
      return {
        "number": this.$store.state.number_columns,
        "text": this.$store.state.text_columns
      }
    }
  },
  methods: {
    hideModal: function() {
      this.$store.commit("set_search_modal", {"is_show": false});
    },
    search: function() {
      this.$store.dispatch("search", {
        "index": 0,
        "search_type": this.search_type,
        "conditions": this.search_conditions
      });
      this.$store.dispatch("search", {
        "index": 1,
        "search_type": this.search_type,
        "conditions": this.search_conditions
      });
    },
    addCondition: function() {
      this.search_conditions.push({
        "data_type": "number",
        "operator": "=",
        "column": 0,
        "value": 0,
      });
    },
    removeCondition: function(i) {
      this.search_conditions.splice(i, 1);
    }
  }
}
</script>

<style lang="scss" scoped>
#search-modal {
  $header_height: 35px;

  $modal-color: #000000;
  $modal-opacity: 0.5;

  $modal-content-width: 60%;
  $modal-content-height: 80%;
  $modal-content-bg-color: #fefefe;
  $modal-content-padding: 32px;

  $modal-title-font-size: 32px;
  $modal-sub-title-font-size: 24px;

  position: fixed;
  width: 100vw;
  height: calc(100vh - #{$header_height});

  .modal-background {
    width: 100%;
    height: 100%;
    background-color: $modal-color;
    opacity: $modal-opacity;
  }

  .modal-content {
    position: absolute;
    top: 50%;
    left: 50%;
    -webkit-transform: translateY(-50%) translateX(-50%);
    transform: translateY(-50%) translateX(-50%);

    width: $modal-content-width;
    height: $modal-content-height;
    padding: $modal-content-padding;
    background-color: $modal-content-bg-color;
    opacity: 1;

    .modal-title {
      font-size: $modal-title-font-size;
    }

    .search-type-area {
      width: 20%;
    }

    .modal-param-area {
      .condition-row {
        display: flex;
      }
    }
  }
}
</style>
