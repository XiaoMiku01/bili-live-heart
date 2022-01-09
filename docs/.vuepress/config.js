module.exports = {
    title: '哔哩哔哩粉丝牌助手',
    description: '哔哩哔哩粉丝牌助手',
    base: '/',
    head: [
        ['link', { rel: 'icon', href: '/logo.png' }],
    ],
    themeConfig: {
        logo: '/logo.png',
        repo: 'XiaoMiku01/bili-live-heart',
        nav: [
            { text: 'Home', link: '/' },
            { text: '指南', link: '/guide/' },
            { text: '常见问题', link: '/qa/' },
        ],
        // search: false,
        sidebar: 'auto',
        editLinkText: '在 GitHub 上编辑此页',
        lastUpdatedText: '上次更新',
        contributorsText: '贡献者',
        editLinks: true,
    }
}

