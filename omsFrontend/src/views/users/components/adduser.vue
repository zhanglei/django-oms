<template xmlns="http://www.w3.org/1999/html">
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
    <el-form-item label="用户名" prop="username">
      <el-input v-model="ruleForm.username"></el-input>
    </el-form-item>
    <el-form-item label="Email" prop="email">
      <el-input v-model="ruleForm.email"></el-input>
    </el-form-item>
    <el-form-item label="Skype" prop="email">
      <el-input v-model="ruleForm.skype"></el-input>
    </el-form-item>
    <el-form-item label="用户分组" prop="group">
      <el-select v-model="ruleForm.group" placeholder="请选择用户分组">
        <el-option v-for="item in groups" :key="item.name" :value="item.name"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="是否激活" prop="is_active">
      <el-switch on-text="oo" off-text="xx" v-model="ruleForm.is_active"></el-switch>
    </el-form-item>
    <el-form-item label="角色" prop="group">
      <el-select v-model="ruleForm.roles" placeholder="请选择用户角色">
        <el-option v-for="item in roles" :key="item.name" :value="item.name"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="postForm('ruleForm')">提交</el-button>
      <el-button type="danger" @click="resetForm('ruleForm')">清空</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import { postUser, getGroup, getRole } from 'api/user'

export default {
  components: {},

  data() {
    return {
      ruleForm: {
        username: '',
        email: '',
        skype: '',
        is_active: '',
        group: '',
        roles: '',
        password: 'qwert@12345'
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        email: [
          { required: true, type: 'email', message: '请输入正确的Email地址', trigger: 'blur' }
        ],
        skype: [
          { required: true, message: '请输入正确的Skype地址', trigger: 'blur' }
        ],
        group: [
          { required: true, message: '请选择用户分组', trigger: 'change' }
        ],
        roles: [
          { required: true, message: '请选择用户角色', trigger: 'blur' }
        ]
      },
      groups: '',
      roles: ''
    }
  },

  created() {
    this.getGroups()
    this.getRoles()
  },
  methods: {
    postForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          postUser(this.ruleForm).then(response => {
            if (response.statusText === 'ok') {
              this.$message({
                type: 'success',
                message: '恭喜你，新建成功'
              })
            }
          }).catch(error => {
            this.$message.error('新建失败')
            console.log(error)
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
      this.$emit('DialogStatus', false)
    },

    resetForm(formName) {
      this.ruleForm.hosts = []
      this.$refs[formName].resetFields()
    },
    getHosts(data) {
      this.ruleForm.hosts = data
    },
    getGroups() {
      getGroup().then(response => {
        this.groups = response.data.results
      })
    },
    getRoles() {
      getRole().then(response => {
        this.roles = response.data.results
      })
    },
    setPasswd() {
      this.ruleForm.password = Math.random().toString(35).slice(2)
    }
  }
}
</script>

<style lang='scss'>

</style>
