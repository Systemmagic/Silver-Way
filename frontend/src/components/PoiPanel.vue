<template>
  <div class="poi-panel">
    <el-card header="生活圈设施管理">
      <div class="panel-section">
        <el-button type="primary" @click="handleAddByClick">在地图上点击添加</el-button>
        <el-button @click="handleRefresh">刷新列表</el-button>
      </div>

      <el-divider />

      <div class="panel-section">
        <h4>当前视野内的设施</h4>
        <el-table :data="poiList" height="800" style="width: 100%" @row-click="handleRowClick">
          <el-table-column prop="id" label="ID" width="50" />
          <el-table-column prop="name" label="名称" />
          <el-table-column prop="type" label="类型" width="100" />
          <el-table-column label="操作" width="120">
            <template #default="{ row }">
              <el-button link type="primary" @click.stop="handleEdit(row)">编辑</el-button>
              <el-button link type="danger" @click.stop="handleDelete(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <el-dialog v-model="editDialogVisible" title="编辑设施信息" width="400px">
        <el-form :model="editForm" label-width="80px">
          <el-form-item label="名称">
            <el-input v-model="editForm.name" />
          </el-form-item>
          <el-form-item label="类型">
            <el-select v-model="editForm.type" placeholder="请选择类型">
              <el-option label="医疗" value="医疗" />
              <el-option label="助餐" value="助餐" />
              <el-option label="生鲜" value="生鲜" />
              <el-option label="公厕" value="公厕" />
              <el-option label="公园" value="公园" />
              <el-option label="其他" value="其他" />
            </el-select>
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitEdit">保存</el-button>
        </template>
      </el-dialog>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { POIGeoJSON } from '../types/poi'
import { fetchPoisByBbox, updatePoi, deletePoi } from '../services/poiApi'

const props = defineProps<{
  bbox: string
}>()

const emit = defineEmits<{
  (e: 'feature-selected', feature: any): void
  (e: 'refresh-map'): void
}>()

const poiList = ref<any[]>([])
const editDialogVisible = ref(false)
const editForm = ref({ id: 0, name: '', type: '' })

async function loadPois() {
  if (!props.bbox) return
  try {
    const data = await fetchPoisByBbox(props.bbox)
    const features = Array.isArray(data?.features) ? data.features : []
    poiList.value = features.map((f: POIGeoJSON) => ({
      id: f.properties.id,
      name: f.properties.name,
      type: f.properties.type,
      geometry: f.geometry
    }))
  } catch (error: any) {
    const message = error?.response?.data?.error || error?.message || '未知错误'
    ElMessage.error(`加载设施列表失败：${message}`)
  }
}

watch(
  () => props.bbox,
  () => {
    loadPois()
  },
  { immediate: true }
)

function handleRefresh() {
  emit('refresh-map')
  loadPois()
}

function handleAddByClick() {
  ElMessage.info('请在地图上点击要添加的位置')
}

function handleRowClick(row: any) {
  emit('feature-selected', { id: row.id, geometry: row.geometry })
}

function handleEdit(row: any) {
  editForm.value = { id: row.id, name: row.name, type: row.type }
  editDialogVisible.value = true
}

async function submitEdit() {
  try {
    await updatePoi(editForm.value.id, {
      name: editForm.value.name,
      type: editForm.value.type
    })
    ElMessage.success('修改成功')
    editDialogVisible.value = false
    handleRefresh()
  } catch (error) {
    ElMessage.error('修改失败')
  }
}

async function handleDelete(row: any) {
  try {
    await ElMessageBox.confirm(`确定删除 "${row.name}" 吗？`, '确认删除', {
      type: 'warning'
    })
    await deletePoi(row.id)
    ElMessage.success('删除成功')
    handleRefresh()
  } catch (error) {
  }
}

onMounted(() => {
  loadPois()
})
</script>

<style scoped>
.poi-panel {
  height: 100%;
  overflow-y: auto;
}

.panel-section {
  margin-bottom: 16px;
}
</style>
