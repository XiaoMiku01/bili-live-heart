module.exports = {
    title: '哔哩哔哩粉丝牌助手',
    description: '哔哩哔哩粉丝牌助手',
    base: '/bili-live-heart/',
    head: [
        ['link', { rel: 'icon', href: '/logo.png' }],
    ],
    themeConfig: {
        logo: '/logo.png',
        repo: 'XiaoMiku01/bili-live-heart',
        nav: [
            { text: '首页', link: '/' },
            { text: '指南', link: '/Guide/' },
            { text: '0基础腾讯云函数部署', link: '/TencentCloud/' },
            { text: '本地部署/Docker', link: '/LocalDocker/' },
            { text: '常见问题', link: '/QA/' },
            { text: '更新日志', link: '/Changelog/' },
        ],
        // search: false,
        sidebar: {
            '/Guide/': [
                '',
                'Cookie',
                'ServerChan',
            ],
            '/TencentCloud/': [
                '',],
            '/LocalDocker/': [
                '',],
            '/QA/': [
                '',],
            '/Changelog/': [
                '',],

        },
        editLinkText: '在 GitHub 上编辑此页',
        lastUpdatedText: '上次更新',
        contributorsText: '贡献者',
        editLinks: true,
    }
}

