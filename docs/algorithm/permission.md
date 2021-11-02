# 权限

## 权限定义

权限描述为`对什么资源进行什么操作`。
ArkID 只记录某对象有无某权限。至于这个结果会有什么影响，完全由应用决定，即 ArkID 不关心权限如何被使用。

比如，某应用将文件访问权限委托 ArkID 维护。用户访问该文件时，应用需向 ArkID 询问此用户有无权限。至于应用不询问、或者不参考 ArkID 的结果，与 ArkID 无关；应用将此权限另做他用，赋予新的含义，也与 ArkID 无关。

## 权限类型

### 应用权限

附着于应用的权限。应用创建时会自动创建一项访问权限。如果该应用开通了 OAuth2.0 登陆，ArkID 会在登陆时判断此人有无访问权限。其他使用方式由应用决定。

另外还可以自定义应用内权限，使用方式完全由应用决定。

### 内置权限

除了替外部应用维护权限外，ArkID 权限系统还负责维护 ArkID 自己的部分权限。
内置权限具体如下：

- 创建用户
- 创建大类
- 创建应用
- 查看日志
- 公司基本信息配置、基础设施配置
- 账号同步

在 WEB 页面上，分配这些内置权限只能通过子管理员组的方式。编辑子管理员组的基础权限，组内的子管理员可以继承获得这些权限。

因为不期望通过常规方式进行自由分配。所以 ArkID 没有将自己注册为一个应用，维护权限。

## 权限计算

**分配操作**，权限可以分配给任意分组（包括部门、角色、标签以及自定义分组）和个人。包括显式授权、显式拒绝、默认三种方式。

**分配结果**，只有是或否两种状态。

- 对于分组：如果有显式操作，则可以直接判定。若无，则与上级节点的分配结果保持一致。
- 对于个人：如果有显式操作，则可以直接判定。无法直接判定的时候，若直属的任一分组有权限，即有；否则则无。