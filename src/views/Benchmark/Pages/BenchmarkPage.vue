<template>
  <el-tabs type="border-card" @tab-click="handleTabClick" :stretch="true" style="min-height: 80vh;">
    <el-tab-pane :key="key" :name="`${method}_${key}`" v-for="(query, key) in commands[method]">
      <span slot="label">
        <v-icon :name="$store.getters.getIcon(key)"/>
        <!-- Newline -->
        {{$_.startCase(key)}}
      </span>
      <h1>
        {{$_.startCase(key)}}
        <el-button
          circle
          icon="el-icon-refresh"
          @click="() => handleClick(`${method}_${key}`)"
          :loading="isLoading"
        ></el-button>
      </h1>
      <span>{{query.sql[0]}}</span>
      <benchmark-pane :data="`${method}_${key}`" :query="query" :reset="reset"/>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import _ from "lodash";
import BenchmarkPane from "@/components/Panes/BenchmarkPane";

export default {
  props: {
    method: String
  },
  components: { BenchmarkPane },
  data() {
    return {
      reset: false,
      isLoading: false,
      commands: {}
    };
  },
  async created() {
    const res = await fetch("/api/commands");
    const commands = await res.json();
    const ncommands = _.map(commands, (methods, dialect) =>
      _.mapValues(methods, queries =>
        _.mapValues(queries, value => ({ [dialect]: value }))
      )
    );
    this.commands = _.merge(...ncommands);
  },
  methods: {
    handleClick: async function(action) {
      this.isLoading = true;

      const res = await fetch(`/api/command/${action}`);
      const json = await res.json();

      this.$set(this.$store.state.executionData, action, json);

      this.isLoading = false;
    },
    handleTabClick: function() {
      this.reset = true;
      this.$nextTick(function() {
        this.reset = false;
      });
    }
  }
};
</script>

<style scoped>
</style>
