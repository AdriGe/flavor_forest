<template>
    <div>
        <h2>All recipe filters</h2>
    </div>
</template>

<script>
import { ref } from 'vue';

export default {
    name: 'MyComponent',
    setup() {
        const title = 'My Component';
        const count = ref(0);

        const incrementCount = () => {
            count.value++;
        };

        return {
            title,
            count,
            incrementCount,
        };
    },
};
</script>
