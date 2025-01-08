<script>
	import Navigation from "../../components/Navigation.svelte";
  import SearchBar from "../../components/SearchBar.svelte";
  import ActionsGrid from "../../components/ActionsGrid.svelte";

</script>

<div class="h-screen flex select-none">
  <div class="flex justify-center items-center w-1/4 h-screen fixed z-10 ml-2 ">
    <Navigation />
  </div>

  <div class="w-3/4 flex justify-center absolute right-0">
    <SearchBar />
    <ActionsGrid />
  </div>
</div>
